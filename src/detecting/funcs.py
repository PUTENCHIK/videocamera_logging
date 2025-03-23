import cv2
import time
import asyncio

from src import Config
from src.cameras import _get_monitoring_cameras
from src.database import DBSession
from src.detecting.tm import task_manager
from src.detecting.model import detecting_model


async def monitor_camera(address: str):
    print(f"Camera task: {address}")
    capture = cv2.VideoCapture(address)
    if not capture.isOpened():
        print(f"Camera {address} isn't opened")
        task_manager.stop_task(address)
        return
    
    task = task_manager.get_task(address)
    try:
        previous_time = time.time()
        while task.running:
            ret, frame = capture.read()
            if not ret:
                print(f"Frame haven't been got. Reconnection: {address}")
                capture.release()
                capture = cv2.VideoCapture(address)
                if not capture.isOpened():
                    print(f"Reconnection failed")
                    await asyncio.sleep(10)
                    continue
                previous_time = time.time()
                continue

            current_time = time.time()
            if current_time - previous_time >= Config.detecting_delay:
                print(f"{current_time}: Detecting objects on {address}")
                results = detecting_model.predict(frame)
                print(f"\tfound {len(results.probs)} in {round(results.time, 3)} s")
                previous_time = current_time
            await asyncio.sleep(0.01)

    except asyncio.CancelledError:
        print(f"Task for {address} canceled")
    except Exception as e:
        print(f"Unknown exception for {address}: {e}")
    finally:
        print(f"Task canceled for {address}")
        capture.release()
        task_manager.stop_task(address)


async def start_camera_monitoring():
    db = DBSession()
    try:
        cameras = _get_monitoring_cameras(db)
        for camera in cameras:
            task = asyncio.create_task(monitor_camera(camera.address))
            task_manager.add_task(camera.address, task)
        
        task_manager.info()
    finally:
        db.close()
