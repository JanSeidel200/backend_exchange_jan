from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_success_sets_cookie():
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "change-me"},
    )
    assert response.status_code == 200
    assert "access_token" in response.cookies


def test_login_invalid_credentials():
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong"},
    )
    assert response.status_code == 401


def test_logout_returns_ok():
    response = client.post("/api/auth/logout")
    assert response.status_code == 200