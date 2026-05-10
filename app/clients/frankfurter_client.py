from typing import Any

import httpx

from app.core.config import settings


class FrankfurterClient:
    def __init__(self) -> None:
        self.base_url = settings.frankfurter_base_url.rstrip("/")

    async def _get(
        self, path: str, params: dict[str, str] | None = None
    ) -> Any:
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_currencies(self) -> dict[str, str]:
        return await self._get("/currencies")