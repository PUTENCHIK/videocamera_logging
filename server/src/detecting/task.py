import cv2
import time
import asyncio
import threading

from numpy import ndarray
from pprint import pprint
from typing import Optional
from datetime import datetime

from src import Config
from src.snapshots import (SnapshotAdd, Bbox, ObjectAdd,
                           _add_object, _add_snapshot)
from src.database import get_db_session
from src.detecting import detecting_model, DetectingResults
from src.cameras import Camera
from src.websockets import message_manager


class DetectingTask:
    def __init__(self,
                 camera: Camera):
        self.camera = camera
        self.capture = None
        self.running = False
        self.lock = threading.Lock()
        self.initialization_thread = None
        self.stop_event = threading.Event()
        self.last_cooldown = None
        self.last_results = None
    
    @property
    def id(self):
        return self.camera.id

    @property
    def address(self):
        return self.camera.address

    def initialize_capture(self):
        self.capture = None
        try:
            print(f"Task {self.id}: Starting initialization of capture...")
            with self.lock:
                self.running = True
            self.capture = cv2.VideoCapture(self.address)
            if not self.capture.isOpened():
                print(f"[WARNING]: task {self.id} could not open RTSP stream.")
                message_manager.swa(f"Камера #{self.id}",
                                    f"Не получилось открыть поток для {self.address}. Перезапуск задачи")
                self.release_capture()
                if self.running:
                    self.start()
            elif self.stop_event.is_set():
                print(f"Task {self.id}: Stop event received during initialization. Releasing resources.")
                self.release_capture()
                with self.lock:
                    self.running = False
                return
            else:
                print(f"Task {self.id}: Capture initialized successfully.")
                self.monitoring()

        except Exception as e:
            print(f"Task {self.id}: Exception during initialization: {e}")
            self.release_capture()

    def start(self):
        print(f"START: Task {self.id}")
        self.stop_event.clear()
        self.initialization_thread = threading.Thread(target=self.initialize_capture)
        self.initialization_thread.start()

    def stop(self):
        print(f"STOP: Task {self.id}")
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

    def cooldown(self,
                 dt: datetime) -> Optional[float]:
        return (None if self.last_cooldown is None
                else (dt - self.last_cooldown).total_seconds())

    def is_cooldown(self,
                    dt: datetime) -> bool:
        cd = self.cooldown(dt)
        return cd is not None and cd <= Config.detecting.cooldown

    def monitoring(self):
        try:
            previous_time = time.perf_counter()
            while self.running:
                with self.lock:
                    if self.stop_event.is_set():
                        self.running = False
                        break

                current_time = time.perf_counter()
                ret, frame = self.capture.read()
                if not ret:
                    print(f"Task {self.id}: Error: Could not read frame. Restarting.")
                    message_manager.swa(f"Камера #{self.id}",
                                        f"Не получилось получить изображение. Перезапуск задачи")
                    break
                if current_time - previous_time >= Config.detecting.delay:
                    dt = datetime.now()
                    results = detecting_model.predict(frame, dt)
                    print(f"{current_time}: ", end='')
                    if results.any_objects:
                        if self.last_cooldown is not None:
                            self.last_results = results
                            print("Saved results while cooldown")
                        if self.is_cooldown(dt):
                            print(f"No saving: {Config.detecting.cooldown - (dt - self.last_cooldown).total_seconds()}")
                        else:
                            print()
                            pprint(results.to_json())
                            self.last_cooldown = dt
                            self.last_results = None
                            self.save_wrapper(results)
                    else:
                        print(f"Task {self.id}: No detections", sep=' ')
                        dt = datetime.now()
                        if self.is_cooldown(dt):
                            print(f"(cd: {self.cooldown(dt)})")
                        else:
                            print
                        if not self.is_cooldown(dt) and self.last_results is not None:
                            print("Saving results from memory")
                            pprint(self.last_results.to_json())
                            self.save_wrapper(self.last_results)
                            self.last_cooldown = None
                            self.last_results = None
                    previous_time = current_time
        finally:
            self.release_capture()
            if self.running:
                print(f"Task {self.id} must run. Restart")
                self.start()
            else:
                self.stop()
    
    def save_wrapper(self, results):
        asyncio.run(self.save(results))
    
    async def save(self,
                   results: DetectingResults):
        print(f"Task {self.id}: saving results")
        results_json = results.to_json()
        async for db in get_db_session():
            try:
                snapshot_scheme = SnapshotAdd(
                    camera_id=self.id,
                    detecting_time=results.time,
                    created_at=results.predicted_at
                )
                new_snapshot = await _add_snapshot(snapshot_scheme, db)
                cv2.imwrite(str(Config.pathes.snapshots / f"{new_snapshot.id}.jpg"),
                            results.frame)
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
                        bbox=bbox,
                        created_at=results.predicted_at
                    )
                    obj = await _add_object(object_scheme, db)
                    print(f"\tobject [{obj.id}] added")
            except Exception as e:
                await db.rollback()
                raise e

    def release_capture(self):
        with self.lock:
            if self.capture:
                self.capture.release()
                self.capture = None
                print(f"Task {self.id}: Capture released.")
