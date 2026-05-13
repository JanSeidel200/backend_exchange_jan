from fastapi.testclient import TestClient

from app.api.routes import settings_api
from app.main import app
from app.models.schemas import UserSettings


class FakeFileStorage:
    def __init__(self, saved=None):
        self.saved = saved

    def load_settings(self):
        return self.saved

    def save_settings(self, data):
        self.saved = data


fake_storage = FakeFileStorage()


def override_storage():
    return fake_storage


client = TestClient(app)


def login():
    return client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "change-me"},
    )


def setup_function():
    fake_storage.saved = None
    app.dependency_overrides.clear()
    client.cookies.clear()


def teardown_function():
    app.dependency_overrides.clear()
    client.cookies.clear()


def test_get_settings_requires_auth():
    response = client.get("/api/settings")
    assert response.status_code == 401


def test_get_settings_returns_defaults_when_no_file():
    app.dependency_overrides[settings_api.get_file_storage] = override_storage
    login()

    response = client.get("/api/settings")

    assert response.status_code == 200
    assert response.json() == {"base": "EUR", "symbols": []}


def test_put_settings_persists():
    app.dependency_overrides[settings_api.get_file_storage] = override_storage
    login()

    response = client.put(
        "/api/settings",
        json={"base": "USD", "symbols": ["EUR", "GBP"]},
    )
    assert response.status_code == 200
    assert response.json() == {"base": "USD", "symbols": ["EUR", "GBP"]}

    get_response = client.get("/api/settings")
    assert get_response.status_code == 200
    assert get_response.json() == {"base": "USD", "symbols": ["EUR", "GBP"]}