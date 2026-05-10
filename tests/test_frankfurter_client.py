import httpx
import pytest
import respx

from app.clients.frankfurter_client import FrankfurterClient


@pytest.mark.asyncio
@respx.mock
async def test_get_currencies_returns_dict():
    respx.get("https://api.frankfurter.dev/v1/currencies").mock(
        return_value=httpx.Response(
            200, json={"EUR": "Euro", "USD": "US Dollar"}
        )
    )
    client = FrankfurterClient()
    result = await client.get_currencies()
    assert result["EUR"] == "Euro"


@pytest.mark.asyncio
@respx.mock
async def test_cache_hit_skips_second_request():
    route = respx.get("https://api.frankfurter.dev/v1/currencies").mock(
        return_value=httpx.Response(200, json={"EUR": "Euro"})
    )
    client = FrankfurterClient()
    await client.get_currencies()
    await client.get_currencies()
    assert route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_retry_on_http_error():
    respx.get("https://api.frankfurter.dev/v1/currencies").mock(
        side_effect=[
            httpx.Response(500),
            httpx.Response(500),
            httpx.Response(200, json={"EUR": "Euro"}),
        ]
    )
    client = FrankfurterClient()
    result = await client.get_currencies()
    assert result["EUR"] == "Euro"