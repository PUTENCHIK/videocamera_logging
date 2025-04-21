import asyncio
from typing import List, Optional
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

    async def send_error(self,
                         websocket: WebSocket,
                         ex: Optional[Exception] = None,
                         title: str = "server error",
                         text: str = "unknown"):
        if ex is not None:
            text = str(ex)
        await websocket.send_json({
            "type": "error",
            "title": title,
            "text": text
        })

    async def send_warning(self,
                           websocket: WebSocket,
                           title: str = "warning",
                           text: str = "unknown"):
        await websocket.send_json({
            "type": "warning",
            "title": title,
            "text": text
        })

    async def send_info(self,
                        websocket: WebSocket,
                        title: str = "info",
                        text: str = "unknown"):
        await websocket.send_json({
            "type": "info",
            "title": title,
            "text": text
        })
    
    async def send_error_all(self,
                             ex: Optional[Exception] = None,
                             title: str = "server error",
                             text: str = "unknown"):
        for connection in self.connections:
            await self.send_error(connection, ex, title, text)
    
    async def send_warning_all(self,
                               title: str = "warning",
                               text: str = "unknown"):
        for connection in self.connections:
            await self.send_warning(connection, title, text)
    
    async def send_info_all(self,
                            title: str = "info",
                            text: str = "unknown"):
        for connection in self.connections:
            await self.send_info(connection, title, text)
    
    def sea(self,
            ex: Optional[Exception] = None,
            title: str = "server error",
            text: str = "unknown"):
        asyncio.run(self.send_error_all(ex, title, text))
    
    def swa(self,
            title: str = "warning",
            text: str = "unknown"):
        asyncio.run(self.send_warning_all(title, text))
    
    def sia(self,
            title: str = "info",
            text: str = "unknown"):
        asyncio.run(self.send_info_all(title, text))


message_manager = MessagesManager()
