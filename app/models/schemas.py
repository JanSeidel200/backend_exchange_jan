from pydantic import BaseModel, Field, field_validator
from datetime import date


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=120)


class LoginResponse(BaseModel):
    username: str
    message: str

class CurrencyOption(BaseModel):
    code: str
    name: str

class CurrencyStat(BaseModel):
    code: str
    latest_rate: float | None
    average_rate: float | None
    min_rate: float | None
    max_rate: float | None
    data_points: int

class AnalyzeRequest(BaseModel):
    base: str = Field(min_length=3, max_length=3)
    symbols: list[str] = Field(min_length=1, max_length=10)
    start_date: date
    end_date: date

    @field_validator("base")
    @classmethod
    def normalize_base(cls, value: str) -> str:
        return value.upper()

    @field_validator("symbols")
    @classmethod
    def normalize_symbols(cls, values: list[str]) -> list[str]:
        normalized = [v.upper() for v in values]
        if len(set(normalized)) != len(normalized):
            raise ValueError("Duplicate currencies are not allowed")
        return normalized

    @field_validator("end_date")
    @classmethod
    def validate_date_order(cls, end_date: date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("End date must be after start date")
        return end_date

class AnalyzeResponse(BaseModel):
    base: str
    start_date: date
    end_date: date
    strongest_currency: str | None
    weakest_currency: str | None
    stats: list[CurrencyStat]
    series: dict[str, dict[str, float]]