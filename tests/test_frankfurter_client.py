from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.clients.frankfurter_client import FrankfurterClient

URL = "https://api.frankfurter.dev/v1/currencies"


def make_response(status_code: int, json_data: dict | None = None) -> httpx.Response:
    return httpx.Response(
        status_code,
        json=json_data,
        request=httpx.Request("GET", URL),
    )


@pytest.mark.asyncio
async def test_get_currencies_returns_dict():
    mock_response = make_response(200, {"EUR": "Euro", "USD": "US Dollar"})
    with patch(
        "httpx.AsyncClient.get",
        new=AsyncMock(return_value=mock_response),
    ):
        client = FrankfurterClient()
        result = await client.get_currencies()
        assert result["EUR"] == "Euro"


@pytest.mark.asyncio
async def test_cache_hit_skips_second_request():
    mock_response = make_response(200, {"EUR": "Euro"})
    mock_get = AsyncMock(return_value=mock_response)
    with patch("httpx.AsyncClient.get", new=mock_get):
        client = FrankfurterClient()
        await client.get_currencies()
        await client.get_currencies()
        assert mock_get.call_count == 1


@pytest.mark.asyncio
async def test_retry_on_http_error():
    responses = [
        make_response(500),
        make_response(500),
        make_response(200, {"EUR": "Euro"}),
    ]
    mock_get = AsyncMock(side_effect=responses)
    with patch("httpx.AsyncClient.get", new=mock_get):
        client = FrankfurterClient()
        result = await client.get_currencies()
        assert result["EUR"] == "Euro"

@pytest.mark.asyncio
async def test_get_latest_rates_returns_rates():
    url = "https://api.frankfurter.dev/v1/latest"
    mock_response = httpx.Response(
        200,
        json={
            "amount": 1.0,
            "base": "EUR",
            "date": "2025-01-15",
            "rates": {"CZK": 25.0, "USD": 1.1},
        },
        request=httpx.Request("GET", url),
    )
    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        client = FrankfurterClient()
        result = await client.get_latest_rates("EUR", ["CZK", "USD"])
        assert result["rates"]["CZK"] == 25.0
        assert result["base"] == "EUR"


@pytest.mark.asyncio
async def test_get_time_series_returns_series():
    from datetime import date

    url = "https://api.frankfurter.dev/v1/2025-01-01..2025-01-02"
    mock_response = httpx.Response(
        200,
        json={
            "amount": 1.0,
            "base": "EUR",
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "rates": {
                "2025-01-01": {"CZK": 24.0},
                "2025-01-02": {"CZK": 26.0},
            },
        },
        request=httpx.Request("GET", url),
    )
    with patch("httpx.AsyncClient.get", new=AsyncMock(return_value=mock_response)):
        client = FrankfurterClient()
        result = await client.get_time_series(
            "EUR", ["CZK"], date(2025, 1, 1), date(2025, 1, 2),
        )
        assert "2025-01-01" in result["rates"]
        assert result["rates"]["2025-01-01"]["CZK"] == 24.0