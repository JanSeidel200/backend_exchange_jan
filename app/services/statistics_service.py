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
    
    def _find_strongest(self, latest_rates):
        if not latest_rates:
            return None
        return max(latest_rates, key=latest_rates.get)

    def _find_weakest(self, latest_rates):
        if not latest_rates:
            return None
        return min(latest_rates, key=latest_rates.get)