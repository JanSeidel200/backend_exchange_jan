from fastapi.testclient import TestClient

from app.api.routes import currency
from app.main import app
from app.models.schemas import CurrencyOption


class FakeCurrencyService:
    async def list_currencies(self):
        return [CurrencyOption(code="EUR", name="Euro")]


def override_service():
    return FakeCurrencyService()


client = TestClient(app)


def login():
    return client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "change-me"},
    )


def test_currencies_requires_auth():
    client.cookies.clear()
    response = client.get("/api/currency/currencies")
    assert response.status_code == 401


def test_currencies_success():
    app.dependency_overrides[currency.get_currency_service] = override_service
    login()
    response = client.get("/api/currency/currencies")
    assert response.status_code == 200
    assert response.json()[0]["code"] == "EUR"
    app.dependency_overrides.clear()