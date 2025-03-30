import cv2
import time
import asyncio

from numpy import ndarray
from pprint import pprint
from typing import Optional, List, Dict, Tuple

from src import Config
from src.cameras import _get_monitoring_cameras
from src.snapshots import (SnapshotAdd, Bbox, ObjectAdd,
                           _add_object, _add_snapshot)
from src.database import get_db_session
from src.detecting.model import detecting_model
from src.detecting import DetectingResults
from src.cameras import Camera


class TaskManager:
    def __init__(self):
        self.__task = None
        self.cameras: Dict[int, Camera] = {}
        self.vcs: Dict[int, cv2.VideoCapture] = {}
        self.lock = asyncio.Lock()

    def set_task(self,
                 task: Optional[asyncio.Task]):
        self.__task = task
    
    async def create_vc(self,
                        address: str) -> cv2.VideoCapture:
        capture = cv2.VideoCapture(address)
        capture.set(cv2.CAP_PROP_VIDEO_STREAM, cv2.CAP_FFMPEG)
        return capture
    
    def info(self):
        print("TaskManager info:")
        cameras = self.cameras
        if len(cameras):
            for i, camera in enumerate(cameras.values()):
                print(f"{i+1}) [{camera.id}] {camera.address}: {self.vcs.get(camera.id, None)}")
        else:
            print("\tno monitoring cameras")

    async def initialize_cameras(self):
        async for db in get_db_session():
            try:
                cameras = {camera.id: camera for camera in await _get_monitoring_cameras(db)}
                async with self.lock:
                    self.cameras = cameras
                print(f"Cameras initialized: {len(self.cameras)}")
            except Exception as e:
                await db.rollback()
                raise e

    async def initialize_vcs(self):
        new_vcs = {}
        for camera in self.cameras.values():
            new_vcs[camera.id] = await self.create_vc(camera.address)
            print(f"VideoCapture initialized for camera [{camera.id}]")
        async with self.lock:
            self.vcs = new_vcs
        print(f"VideoCaptures initialized: {len(self.vcs)}")
    
    async def edit_camera(self,
                          camera: Camera):
        if camera.id in self.cameras:
            new_vc = await self.create_vc(camera.address)
            async with self.lock:
                self.cameras[camera.id] = camera
                self.vcs[camera.id] = new_vc
            print(f"VideoCapture recreated for camera [{camera.id}]")
        else:
            print(f"[WARNING] [{camera.id}] not in cameras")
    
    async def delete_camera(self,
                            camera: Camera):
        if camera.id in self.cameras:
            self.vcs[camera.id].release()
            async with self.lock:
                self.cameras.pop(camera.id)
                self.vcs.pop(camera.id)
            print(f"Camera and VideoCapture deleted for [{camera.id}]")
        else:
            print(f"[WARNING] [{camera.id}] not in cameras")
    
    async def switch_camera(self,
                            camera: Camera):
        if camera.id not in self.cameras and camera.is_monitoring:
            new_vc = await self.create_vc(camera.address)
            async with self.lock:
                self.cameras[camera.id] = camera
                self.vcs[camera.id] = new_vc
            print(f"Camera switched on for [{camera.id}]")
        elif camera.id in self.cameras and not camera.is_monitoring:
            await self.delete_camera(camera)
            print(f"Camera switched off for [{camera.id}]")

    def release_all_vcs(self):
        for camera_id, vc in self.vcs.items():
            vc.release()
            print(f"camera [{camera_id}]: released")

    async def reopen_vc(self,
                        camera_id: int):
        print(f"Trying to reopen VideoCapture for [{camera_id}]")
        new_vc = await self.create_vc(self.cameras[camera_id].address)
        async with self.lock:
            self.vcs[camera_id] = new_vc
        print(f"VideoCapture recreated for camera [{camera_id}]")

    async def get_frames(self) -> Tuple[List[int], List[ndarray]]:
        cameras_id, frames = [], []
        for camera_id, vc in list(self.vcs.items()):
            if not vc.isOpened():
                print(f"camera [{camera_id}]: is not opened")
                asyncio.create_task(self.reopen_vc(camera_id))
            else:
                ret, frame = vc.read()
                if ret is None or frame is None:
                    print(f"camera [{camera_id}]: frame has not been gotten")
                    asyncio.create_task(self.reopen_vc(camera_id))
                else:
                    cameras_id += [camera_id]
                    frames += [frame]
        return cameras_id, frames
    
    async def start(self):
        print("start_task called")
        init_cameras = asyncio.create_task(self.initialize_cameras())
        print("init_cameras task created")
        await init_cameras
        print("Cameras initialization ended, creating vcs task")
        asyncio.create_task(self.initialize_vcs())
        if self.__task is None or self.__task.cancelled():
            task = asyncio.create_task(self.monitor_cameras())
            self.set_task(task)
        self.info()
    
    async def kill_task(self):
        if self.__task is not None:
            self.__task.cancel()
        self.release_all_vcs()
        self.set_task(None)
    
    async def monitor_cameras(self):
        print(f"Camera Monitoring started")
        try:
            previous_time = time.perf_counter()
            while not self.__task.cancelled():
                cameras_id, frames = await self.get_frames()
                current_time = time.perf_counter()
                if len(frames) and current_time - previous_time >= Config.model.detecting_delay:
                    results = detecting_model.predict(source=frames,
                                                      ids=cameras_id)
                    print(f"{current_time}: ", end='')
                    if results.any_objects:
                        print()
                        pprint(results.to_json())
                        asyncio.create_task(self.save_results(results, frames))
                    else:
                        print("no detections")
                    previous_time = current_time

                await asyncio.sleep(0.01)

        except asyncio.CancelledError:
            print(f"CancelledError catched")
        finally:
            print(f"Task ended")
            await self.kill_task()

    async def save_results(self,
                           results: DetectingResults,
                           frames: List[ndarray]):
        results_json = results.to_json()
        async for db in get_db_session():
            try:
                for i, (camera_id, objects) in enumerate(results_json["results"].items()):
                    if len(objects):
                        snapshot_scheme = SnapshotAdd(
                            camera_id=camera_id,
                            detecting_time=results.time
                        )
                        new_snapshot = await _add_snapshot(snapshot_scheme, db)
                        cv2.imwrite(str(Config.pathes.snapshots / f"{new_snapshot.id}.jpg"), frames[i])
                        print(f"Snapshot [{new_snapshot.id}] added")
                        for object in objects:
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


task_manager = TaskManager()
