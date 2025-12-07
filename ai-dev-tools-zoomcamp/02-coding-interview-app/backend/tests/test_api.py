import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_session(client: AsyncClient):
    response = await client.post("/sessions/", json={"language": "python"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["language"] == "python"
    assert "code_content" in data

@pytest.mark.asyncio
async def test_get_session(client: AsyncClient):
    # Create a session first
    create_response = await client.post("/sessions/", json={"language": "javascript"})
    session_id = create_response.json()["id"]
    
    # Get the session
    response = await client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert data["language"] == "javascript"

@pytest.mark.asyncio
async def test_execute_code_python(client: AsyncClient):
    code = "print('Hello Test')"
    response = await client.post("/execute", json={"code": code, "language": "python"})
    assert response.status_code == 200
    data = response.json()
    assert "Hello Test" in data["output"]

@pytest.mark.asyncio
async def test_execute_code_unsupported(client: AsyncClient):
    response = await client.post("/execute", json={"code": "foo", "language": "ruby"})
    assert response.status_code == 200
    data = response.json()
    assert "Unsupported Language" in data["error"]
