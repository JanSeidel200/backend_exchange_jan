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