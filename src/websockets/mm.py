from typing import List
from fastapi import WebSocket


class MessagesManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self,
                      websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self,
                   websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_error_message(self,
                                 websocket: WebSocket,
                                 ex: Exception = None,
                                 title: str = "server error",
                                 text: str = "unknown"):
        if ex is not None:
            text = str(ex)
        await websocket.send_json({
            "type": "error",
            "title": title,
            "text": text
        })

    async def broadcast(self,
                        message: str):
        for connection in self.connections:
            await connection.send_text(message)


message_manager = MessagesManager()
