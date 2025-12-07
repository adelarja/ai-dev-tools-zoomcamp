import pytest
from httpx import AsyncClient
from httpx_ws import aconnect_ws
from app.main import app

@pytest.mark.asyncio
async def test_websocket_flow(client: AsyncClient):
    # 1. Create a session
    response = await client.post("/sessions/", json={"language": "python"})
    assert response.status_code == 200
    session_id = response.json()["id"]
    
    # 2. Connect to WebSocket
    # We need to construct the WS URL. client.base_url is http://test
    # WS URL should be ws://test/ws/{session_id}
    
    # Note: aconnect_ws needs the app if we want to test ASGI directly without a running server?
    # Or we can pass the client.
    
    async with aconnect_ws(f"ws://test/ws/{session_id}", client) as ws:
        # 3. Send a code update
        payload = {"type": "code", "payload": "print('Hello WS')"}
        await ws.send_json(payload)
        
        # 4. Receive broadcast
        message = await ws.receive_json()
        assert message["type"] == "code"
        assert message["payload"] == "print('Hello WS')"
        
    # 5. Verify DB update via API
    response = await client.get(f"/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json()["code_content"] == "print('Hello WS')"

@pytest.mark.asyncio
async def test_websocket_language_sync(client: AsyncClient):
    # 1. Create session
    response = await client.post("/sessions/", json={"language": "python"})
    session_id = response.json()["id"]
    
    # 2. Connect
    async with aconnect_ws(f"ws://test/ws/{session_id}", client) as ws:
        # 3. Send language update
        payload = {"type": "language", "payload": "javascript"}
        await ws.send_json(payload)
        
        # 4. Receive broadcast
        message = await ws.receive_json()
        assert message["type"] == "language"
        assert message["payload"] == "javascript"
        
    # 5. Verify DB update
    response = await client.get(f"/sessions/{session_id}")
    assert response.json()["language"] == "javascript"
