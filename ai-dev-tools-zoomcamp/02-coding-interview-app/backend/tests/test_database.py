import pytest
from sqlalchemy import select
from app.models import InterviewSession
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_session_db(db_session: AsyncSession):
    new_session = InterviewSession(language="python", code_content="print('Hello DB')")
    db_session.add(new_session)
    await db_session.commit()
    await db_session.refresh(new_session)
    
    assert new_session.id is not None
    assert new_session.language == "python"
    assert new_session.code_content == "print('Hello DB')"

@pytest.mark.asyncio
async def test_get_session_db(db_session: AsyncSession):
    # Create
    session = InterviewSession(language="java", code_content="class Main {}")
    db_session.add(session)
    await db_session.commit()
    
    # Retrieve
    stmt = select(InterviewSession).where(InterviewSession.id == session.id)
    result = await db_session.execute(stmt)
    retrieved = result.scalars().first()
    
    assert retrieved is not None
    assert retrieved.id == session.id
    assert retrieved.language == "java"

@pytest.mark.asyncio
async def test_update_session_db(db_session: AsyncSession):
    session = InterviewSession(language="cpp", code_content="int main() {}")
    db_session.add(session)
    await db_session.commit()
    
    # Update
    session.code_content = "updated code"
    await db_session.commit()
    await db_session.refresh(session)
    
    assert session.code_content == "updated code"
