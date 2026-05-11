from datetime import date

from app.models.schemas import AnalyzeResponse, CurrencyStat


class StatisticsService:
    def analyze(
        self,
        base: str,
        symbols: list[str],
        start_date: date,
        end_date: date,
        latest_rates: dict[str, float],
        series: dict[str, dict[str, float]],
    ) -> AnalyzeResponse:
        raise NotImplementedError