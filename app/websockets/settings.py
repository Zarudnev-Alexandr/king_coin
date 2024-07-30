import asyncio

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.tasks: dict[int, asyncio.Task] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        # Закрыть существующее соединение, если оно уже есть
        if existing_websocket := self.active_connections.get(user_id):
            await existing_websocket.close()

        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        # Отменить существующую задачу, если она есть
        if task := self.tasks.pop(user_id, None):
            task.cancel()
        self.active_connections.pop(user_id, None)

    async def send_message(self, message: dict, user_id: int):
        if websocket := self.active_connections.get(user_id):
            await websocket.send_json(message)

    async def notify_user(self, user_id: int, message: dict):
        await self.send_message(message, user_id)


ws_manager = ConnectionManager()
