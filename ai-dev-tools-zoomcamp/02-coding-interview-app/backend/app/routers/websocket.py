from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import InterviewSession
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

    async def broadcast_json(self, message: dict, session_id: str, sender: WebSocket):
        if session_id in self.active_connections:
            for connection in self.active_connections[session_id]:
                if connection != sender:
                    await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, db: AsyncSession = Depends(get_db)):
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_json()
            
            # Update code/language in DB
            stmt = select(InterviewSession).where(InterviewSession.id == session_id)
            result = await db.execute(stmt)
            session = result.scalars().first()
            
            if session:
                if data.get("type") == "code":
                    session.code_content = data.get("payload")
                elif data.get("type") == "language":
                    session.language = data.get("payload")
                await db.commit()
            
            # Broadcast the JSON message as is
            await manager.broadcast_json(data, session_id, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
