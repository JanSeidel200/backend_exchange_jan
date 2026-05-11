from datetime import date

from app.models.schemas import AnalyzeResponse, CurrencyStat


class StatisticsService:
    def analyze(
        self,
        base,
        symbols,
        start_date,
        end_date,
        latest_rates,
        series,
    ) -> AnalyzeResponse:
        strongest = self._find_strongest(latest_rates)
        weakest = self._find_weakest(latest_rates)
        stats = [
            self._calculate_currency_stat(
                symbol, latest_rates.get(symbol), series
            )
            for symbol in symbols
        ]
        return AnalyzeResponse(
            base=base,
            start_date=start_date,
            end_date=end_date,
            strongest_currency=strongest,
            weakest_currency=weakest,
            stats=stats,
            series=series,
        )
    
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