from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_kakao_login():
    params = {
        "code" : "my_code"
    }
    response = client.get("/api/v1/kakao/login", params=params)

    assert response.status_code == 200
    data = response.json()

    # Assert that the response contains the expected keys
    assert "user" in data
    assert "tokenInfo" in data

    # Assert the structure and content of the user object
    user = data["user"]
    assert "id" in user
    assert "name" in user
    assert "email" in user

    # Assert the structure and content of the tokenInfo object
    token_info = data["tokenInfo"]
    assert "access_token" in token_info
    assert "expires_in" in token_info
    assert "token_type" in token_info
