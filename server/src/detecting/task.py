import cv2
import time
import asyncio
import threading

from numpy import ndarray
from pprint import pprint

from src import Config
from src.snapshots import (SnapshotAdd, Bbox, ObjectAdd,
                           _add_object, _add_snapshot)
from src.database import get_db_session
from src.detecting import detecting_model, DetectingResults
from src.cameras import Camera


class DetectingTask:
    def __init__(self,
                 camera: Camera):
        self.camera = camera
        self.capture = None
        self.running = False
        self.lock = threading.Lock()
        self.initialization_thread = None
        self.stop_event = threading.Event()
    
    @property
    def id(self):
        return self.camera.id

    def initialize_capture(self):
        self.capture = None
        try:
            print(f"Task {self.id}: Starting initialization of capture...")
            self.capture = cv2.VideoCapture(self.camera.address)
            if self.stop_event.is_set():
                print(f"Task {self.id}: Stop event received during initialization. Releasing resources.")
                self.release_capture()
                return
            if not self.capture.isOpened():
                print(f"[ERROR]: task {self.id} could not open RTSP stream.")
                self.release_capture()
                return

            with self.lock:
                self.running = True
            print(f"Task {self.id}: Capture initialized successfully.")
            self.monitoring()

        except Exception as e:
            print(f"Task {self.id}: Exception during initialization: {e}")
            self.release_capture()

    def start(self):
        self.stop_event.clear()
        self.initialization_thread = threading.Thread(target=self.initialize_capture)
        self.initialization_thread.start()

    def stop(self):
        with self.lock:
            self.running = False
        self.stop_event.set()
        print(f"Task {self.id}: Stop requested.")

        if self.initialization_thread and self.initialization_thread.is_alive():
            print(f"Task {self.id}: Waiting for initialization thread to finish...")
            self.initialization_thread.join(timeout=5)
            if self.initialization_thread.is_alive():
                print(f"Task {self.id}: Initialization thread did not finish in time.  Potential resource leak.")


        self.release_capture()
        print(f"Task {self.id}: Task stopped.")

    def monitoring(self):
        try:
            previous_time = time.perf_counter()
            while self.running:
                with self.lock:
                    if not self.running or self.stop_event.is_set():
                        break

                current_time = time.perf_counter()
                ret, frame = self.capture.read()
                if not ret:
                    print(f"Task {self.id}: Error: Could not read frame. Releasing resources.")
                    break
                if current_time - previous_time >= Config.model.detecting_delay:
                    results = detecting_model.predict(frame)
                    print(f"{current_time}: ", end='')
                    if results.any_objects:
                        print()
                        pprint(results.to_json())
                        self.save_wrapper(results, frame)
                    else:
                        print(f"\tTask {self.id}: No detections")
                    previous_time = current_time
        finally:
            self.stop()
            self.start()
    
    def save_wrapper(self, results, frame):
        asyncio.run(self.save(results, frame))
    
    async def save(self,
                   results: DetectingResults,
                   frame: ndarray):
        print(f"Task {self.id}: saving results")
        results_json = results.to_json()
        async for db in get_db_session():
            try:
                snapshot_scheme = SnapshotAdd(
                    camera_id=self.id,
                    detecting_time=results.time
                )
                new_snapshot = await _add_snapshot(snapshot_scheme, db)
                cv2.imwrite(str(Config.pathes.snapshots / f"{new_snapshot.id}.jpg"), frame)
                print(f"Snapshot [{new_snapshot.id}] saved")
                for object in results_json['objects']:
                    x1, y1, x2, y2 = object["box"]
                    bbox = Bbox(
                        x1=x1, y1=y1,
                        x2=x2, y2=y2,
                    )
                    object_scheme = ObjectAdd(
                        snapshot_id=new_snapshot.id,
                        label=object["label"],
                        probability=object["prob"],
                        bbox=bbox
                    )
                    obj = await _add_object(object_scheme, db)
                    print(f"\tobject [{obj.id}] added")
            except Exception as e:
                await db.rollback()
                raise e

    def release_capture(self):
        """Освобождает ресурсы cv2.VideoCapture."""
        with self.lock:
            if self.capture:
                self.capture.release()
                self.capture = None
                print(f"Task {self.id}: Capture released.")
