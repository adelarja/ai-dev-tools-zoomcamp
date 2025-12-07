import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, DATABASE_URL
import asyncio

# Create a new engine for testing to avoid loop issues
# We use the same URL but you might want a separate test DB

@pytest.fixture
async def db_engine():
    engine = create_async_engine(DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    # Connect to the database
    connection = await db_engine.connect()
    # Begin a non-ORM transaction
    transaction = await connection.begin()
    
    # Bind an individual Session to the connection
    # We need to recreate sessionmaker since it binds to engine? 
    # Actually sessionmaker can bind to connection.
    TestingSessionLocal = sessionmaker(bind=connection, class_=AsyncSession, expire_on_commit=False)
    session = TestingSessionLocal()
    
    # Begin a nested transaction (savepoint)
    await session.begin_nested()
    
    yield session
    
    await session.close()
    # Rollback the outer transaction
    await transaction.rollback()
    await connection.close()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()
