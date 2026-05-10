from app.clients.frankfurter_client import FrankfurterClient
from app.models.schemas import CurrencyOption


class CurrencyService:
    def __init__(self, client: FrankfurterClient | None = None) -> None:
        self.client = client or FrankfurterClient()

    async def list_currencies(self) -> list[CurrencyOption]:
        currencies = await self.client.get_currencies()
        return [
            CurrencyOption(code=code, name=name)
            for code, name in sorted(currencies.items())
        ]