from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import InterviewSession
from pydantic import BaseModel

router = APIRouter(prefix="/sessions", tags=["sessions"])

class SessionCreate(BaseModel):
    language: str = "python"

class SessionResponse(BaseModel):
    id: str
    code_content: str
    language: str

    class Config:
        from_attributes = True

@router.post("/", response_model=SessionResponse)
async def create_session(session_in: SessionCreate, db: AsyncSession = Depends(get_db)):
    new_session = InterviewSession(language=session_in.language)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InterviewSession).where(InterviewSession.id == session_id))
    session = result.scalars().first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
