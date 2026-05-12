from fastapi.testclient import TestClient

from app.main import app
from app.core.logging_config import in_memory_handler

client = TestClient(app)


def login() -> None:
    client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "change-me"},
    )


def test_logs_require_auth() -> None:
    client.cookies.clear()

    response = client.get("/api/logs")

    assert response.status_code == 401


def test_logs_return_recent_records_for_admin() -> None:
    client.cookies.clear()
    in_memory_handler.records.clear()

    expected_first = "2026-05-12 21:00:00 | INFO | app.test | first log"
    expected_second = "2026-05-12 21:00:01 | WARNING | app.test | second log"

    in_memory_handler.records.append(expected_first)
    in_memory_handler.records.append(expected_second)

    login()
    response = client.get("/api/logs")

    assert response.status_code == 200

    logs = response.json()["logs"]
    assert expected_first in logs
    assert expected_second in logs


def test_logs_return_list_for_admin_even_when_other_logs_are_added() -> None:
    client.cookies.clear()
    in_memory_handler.records.clear()

    login()
    response = client.get("/api/logs")

    assert response.status_code == 200
    assert "logs" in response.json()
    assert isinstance(response.json()["logs"], list)