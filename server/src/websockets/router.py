from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src import Config
from src.websockets import message_manager


websockets_router = APIRouter(prefix=f"/{Config.routers.websockets_name}",
                              tags=[Config.routers.websockets_name])


@websockets_router.websocket("/messages")
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
