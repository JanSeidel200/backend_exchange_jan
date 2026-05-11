from fastapi.testclient import TestClient

from app.api.routes import currency
from app.main import app
from app.models.schemas import CurrencyOption, AnalyzeRequest, AnalyzeResponse, CurrencyStat



class FakeCurrencyService:
    async def list_currencies(self):
        return [CurrencyOption(code="EUR", name="Euro")]

    async def analyze(self, request: AnalyzeRequest):
        return AnalyzeResponse(
            base=request.base,
            start_date=request.start_date,
            end_date=request.end_date,
            strongest_currency="CZK",
            weakest_currency="USD",
            stats=[
                CurrencyStat(
                    code="CZK",
                    latest_rate=25.0,
                    average_rate=25.0,
                    min_rate=24.0,
                    max_rate=26.0,
                    data_points=2,
                )
            ],
            series={"2025-01-01": {"CZK": 24.0}},
        )


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

def test_analyze_success():
    app.dependency_overrides[currency.get_currency_service] = override_service
    login()
    response = client.post(
        "/api/currency/analyze",
        json={
            "base": "EUR",
            "symbols": ["CZK"],
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
        },
    )
    assert response.status_code == 200
    assert response.json()["strongest_currency"] == "CZK"
    app.dependency_overrides.clear()


def test_analyze_validates_date_order():
    login()
    response = client.post(
        "/api/currency/analyze",
        json={
            "base": "EUR",
            "symbols": ["CZK"],
            "start_date": "2025-01-10",
            "end_date": "2025-01-01",
        },
    )
    assert response.status_code == 422