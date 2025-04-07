from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src import (Config, classes_router, snapshots_router,
                 cameras_router, websockets_router)
from src.detecting import task_manager
from src.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting")
    await create_db_and_tables()        
    # asyncio.create_task(task_manager.start())
    # print("Cameras task added")
    yield
    print("App terminating")
    await task_manager.kill_task()


app = FastAPI(lifespan=lifespan)

app.include_router(classes_router)
app.include_router(snapshots_router)
app.include_router(cameras_router)
app.include_router(websockets_router)

app.mount("/storage/snapshots",
          StaticFiles(directory=Config.pathes.snapshots),
          name="snapshots")

app.add_middleware(CORSMiddleware,
                   allow_origins=Config.app.origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
