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
    
    def _calculate_currency_stat(self, code, latest_rate, series):
        values = []
        for rates_for_day in series.values():
            rate = rates_for_day.get(code)
            if rate is not None:
                values.append(rate)
        average_rate = sum(values) / len(values) if values else None
        return CurrencyStat(
            code=code,
            latest_rate=latest_rate,
            average_rate=average_rate,
            min_rate=min(values) if values else None,
            max_rate=max(values) if values else None,
            data_points=len(values),
        )