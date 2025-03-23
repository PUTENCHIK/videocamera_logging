import asyncio
from typing import Optional


class MyTask:
    def __init__(
            self,
            address: str,
            task: asyncio.Task):
        self.address = address
        self.task = task
        self.running = True


class TaskManager:
    def __init__(self):
        self.__tasks = []

    def add_task(self, address: str, task: asyncio.Task):
        self.__tasks += [MyTask(address, task)]

    def info(self):
        for i, task in enumerate(self.__tasks):
            print(f"{i+1}) {task.address}: "\
                  f"{'running' if task.running else 'canceled'}")
    
    def get_task(self, address: str) -> Optional[MyTask]:
        for task in self.__tasks:
            if task.address == address:
                return task
        return None
    
    def stop_task(self, address: str):
        task = self.get_task(address)
        if task is not None:
            task.running = False
            task.task.cancel()


task_manager = TaskManager()
