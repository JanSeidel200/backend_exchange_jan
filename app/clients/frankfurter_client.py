import time
from typing import Any

import httpx

from app.core.config import settings

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)


class FrankfurterClient:
    def __init__(self) -> None:
        self.base_url = settings.frankfurter_base_url.rstrip("/")
        self._cache: dict[str, tuple[float, Any]] = {}

    def _cache_get(self, key: str) -> Any | None:
        cached = self._cache.get(key)
        if not cached:
            return None
        timestamp, value = cached
        if time.time() - timestamp > settings.cache_ttl_seconds:
            self._cache.pop(key, None)
            return None
        return value

    def _cache_set(self, key: str, value: Any) -> None:
        self._cache[key] = (time.time(), value)


    @retry(
        retry=retry_if_exception_type(httpx.HTTPError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        reraise=True,
    )
    async def _get(
        self, path: str, params: dict[str, str] | None = None
    ) -> Any:
        cache_key = f"{path}:{params}"
        cached = self._cache_get(cache_key)
        if cached is not None:
            return cached
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        self._cache_set(cache_key, data)
        return data

    async def get_currencies(self) -> dict[str, str]:
        return await self._get("/currencies")