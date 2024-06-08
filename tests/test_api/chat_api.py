from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_chat_with_gpt():
    response = client.post("/v1/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert "response" in response.json()
