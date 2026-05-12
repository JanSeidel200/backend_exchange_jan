from fastapi import APIRouter, Depends, Request

from app.core.security import get_current_admin
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, CurrencyOption
from app.services.currency_service import CurrencyService
from app.core.config import settings
from app.core.rate_limit import limiter

router = APIRouter()


def get_currency_service() -> CurrencyService:
    return CurrencyService()


@router.get("/currencies", response_model=list[CurrencyOption])
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def currencies(
    request: Request,
    admin: str = Depends(get_current_admin),
    service: CurrencyService = Depends(get_currency_service),
) -> list[CurrencyOption]:
    return await service.list_currencies()

@router.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def analyze(
    request: Request,
    payload: AnalyzeRequest,
    admin: str = Depends(get_current_admin),
    service: CurrencyService = Depends(get_currency_service),
) -> AnalyzeResponse:
    return await service.analyze(payload)