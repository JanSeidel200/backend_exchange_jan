from app.clients.frankfurter_client import FrankfurterClient
from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    CurrencyOption,
)
from app.services.statistics_service import StatisticsService
from app.storage.file_storage import FileStorage


class CurrencyService:
    def __init__(
        self,
        client: FrankfurterClient | None = None,
        statistics_service: StatisticsService | None = None,
        storage: FileStorage | None = None,
    ) -> None:
        self.client = client or FrankfurterClient()
        self.statistics_service = statistics_service or StatisticsService()
        self.storage = storage or FileStorage()

    async def list_currencies(self) -> list[CurrencyOption]:
        currencies = await self.client.get_currencies()
        return [
            CurrencyOption(code=code, name=name)
            for code, name in sorted(currencies.items())
        ]

    async def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        latest_payload = await self.client.get_latest_rates(
            request.base, request.symbols
        )
        series_payload = await self.client.get_time_series(
            request.base,
            request.symbols,
            request.start_date,
            request.end_date,
        )
        
        result = self.statistics_service.analyze(
            base=request.base,
            symbols=request.symbols,
            start_date=request.start_date,
            end_date=request.end_date,
            latest_rates=latest_payload.get("rates", {}),
            series=series_payload.get("rates", {}),
        )
        
        self.storage.append_analysis_history(
            request=request.model_dump(mode="json"),
            response=result.model_dump(mode="json"),
        )
        
        self.storage.save_settings(
            {"base": request.base, "symbols": request.symbols}
        )
        
        return result