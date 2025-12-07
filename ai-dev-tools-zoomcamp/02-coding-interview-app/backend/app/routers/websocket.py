from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict

router = APIRouter(tags=["websocket"])

class ConnectionManager:
    def __init__(self):
        # Map session_id to list of WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: str):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, message: str, session_id: str, sender: WebSocket):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                if connection != sender:
                    await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Here we would also update the DB state ideally, or just broadcast
            await manager.broadcast(data, session_id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
