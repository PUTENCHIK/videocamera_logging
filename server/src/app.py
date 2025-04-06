import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src import (Config, classes_router, snapshots_router,
                 cameras_router)
from src.detecting import task_manager
from src.database import create_db_and_tables
from src.websockets import message_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting")
    await create_db_and_tables()        
    asyncio.create_task(task_manager.start())
    print("Cameras task added")
    yield
    print("App terminating")
    await task_manager.kill_task()


app = FastAPI(lifespan=lifespan)

app.include_router(classes_router)
app.include_router(snapshots_router)
app.include_router(cameras_router)

app.mount("/storage/snapshots",
          StaticFiles(directory=Config.pathes.snapshots),
          name="snapshots")

app.add_middleware(CORSMiddleware,
                   allow_origins=Config.app.origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.websocket("/ws")
async def wb_messages(websocket: WebSocket):
    await message_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"WebSocket messages received: {data}")
    except WebSocketDisconnect:
        message_manager.disconnect(websocket)
        print("Client disconnected")
    except Exception as e:
        error_message = f"Error: {type(e).__name__} - {str(e)}"
        await message_manager.send_error(websocket, e)
        print(f"Error occurred: {error_message}")
        message_manager.disconnect(websocket)
