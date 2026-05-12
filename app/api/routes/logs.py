from fastapi import APIRouter, Depends, Request

from app.core.config import settings
from app.core.logging_config import in_memory_handler
from app.core.rate_limit import limiter
from app.core.security import get_current_admin

router = APIRouter()


@router.get("/logs")
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
def get_logs(
    request: Request,
    admin: str = Depends(get_current_admin),
) -> dict[str, list[str]]:
    return {"logs": list(in_memory_handler.records)}