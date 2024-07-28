from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        # Если уже есть активное соединение, закрываем его
        if user_id in self.active_connections:
            await self.disconnect(user_id)
        await websocket.accept()
        self.active_connections[user_id] = websocket

    async def disconnect(self, user_id: int):
        websocket = self.active_connections.pop(user_id, None)
        if websocket:
            try:
                await websocket.close()
            except Exception as e:
                print(f"Error closing websocket: {e}")

    async def send_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except RuntimeError as e:
                # Обработка исключения при попытке отправить данные через закрытое соединение
                print(f"Error sending message: {e}")
                await self.disconnect(user_id)

    async def receive_message(self, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            return await websocket.receive_json()


ws_manager = ConnectionManager()
