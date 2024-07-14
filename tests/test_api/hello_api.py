from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_hello():
    response = client.get("/api/hello")
    assert response.status_code == 200
    res_body = response.json()

    assert "data" in res_body
    data = res_body["data"]
    assert data == "hello"
