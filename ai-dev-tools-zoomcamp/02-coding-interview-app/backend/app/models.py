from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base
import uuid

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    code_content = Column(Text, default="")
    language = Column(String, default="python")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
