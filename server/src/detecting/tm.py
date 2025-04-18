import concurrent.futures

from typing import Dict

from src import Config
from src.detecting.task import DetectingTask
from src.cameras import Camera


class TaskManager:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=Config.app.max_detecting_workers
        )
        self.tasks: Dict[int, DetectingTask] = dict()

    async def add_task(self,
                       camera: Camera):
        if camera.id not in self.tasks:
            task = DetectingTask(camera)
            self.tasks[camera.id] = task
            task.start()
            print(f"Task {task.id} added and starting initialization.")
            self.info()
        else:
            print(f"[WARNING] Task {camera.id} already exists")

    async def stop_task(self, task_id: int):
        if task_id in self.tasks:
            self.tasks[task_id].stop()
            self.tasks.pop(task_id, None)
            self.info()
        else:
            print(f"Task with ID {task_id} not found.")

    async def stop_all_tasks(self):
        for task in self.tasks.values():
            task.stop()
        self.tasks = []
        print("All tasks stopped")
    
    def info(self):
        print("=== INFO BLOCK ===")
        for task in self.tasks.values():
            print(f"Task {task.id}:")
            print(f"\t{task.running}")
            print(f"\t{task.camera}")
            print(f"\t{task.capture}")
        print("==== END INFO ====")


task_manager = TaskManager()
