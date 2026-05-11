from fastapi import APIRouter, Depends

from app.core.security import get_current_admin
from app.models.schemas import AnalyzeRequest, AnalyzeResponse, CurrencyOption
from app.services.currency_service import CurrencyService

router = APIRouter()


def get_currency_service() -> CurrencyService:
    return CurrencyService()


@router.get("/currencies", response_model=list[CurrencyOption])
async def currencies(
    admin: str = Depends(get_current_admin),
    service: CurrencyService = Depends(get_currency_service),
) -> list[CurrencyOption]:
    return await service.list_currencies()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    payload: AnalyzeRequest,
    admin: str = Depends(get_current_admin),
    service: CurrencyService = Depends(get_currency_service),
) -> AnalyzeResponse:
    return await service.analyze(payload)