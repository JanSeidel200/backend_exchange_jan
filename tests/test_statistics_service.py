from datetime import date

from app.services.statistics_service import StatisticsService


def test_analyze_calculates_strongest_weakest_and_average():
    service = StatisticsService()
    result = service.analyze(
        base="EUR",
        symbols=["CZK", "USD"],
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 2),
        latest_rates={"CZK": 25.0, "USD": 1.1},
        series={
            "2025-01-01": {"CZK": 24.0, "USD": 1.0},
            "2025-01-02": {"CZK": 26.0, "USD": 1.2},
        },
    )
    assert result.strongest_currency == "CZK"
    assert result.weakest_currency == "USD"
    czk = next(item for item in result.stats if item.code == "CZK")
    assert czk.average_rate == 25.0
    assert czk.min_rate == 24.0
    assert czk.max_rate == 26.0


def test_analyze_ignores_missing_days():
    service = StatisticsService()
    result = service.analyze(
        base="EUR",
        symbols=["CZK"],
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 3),
        latest_rates={"CZK": 25.0},
        series={
            "2025-01-01": {"CZK": 24.0},
            "2025-01-02": {},
            "2025-01-03": {"CZK": 26.0},
        },
    )
    assert result.stats[0].data_points == 2


def test_empty_rates_return_none():
    service = StatisticsService()
    result = service.analyze(
        base="EUR",
        symbols=["CZK"],
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 1),
        latest_rates={},
        series={},
    )
    assert result.strongest_currency is None
    assert result.stats[0].average_rate is None