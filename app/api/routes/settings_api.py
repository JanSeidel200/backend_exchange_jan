from fastapi import APIRouter, Depends, Request

from app.core.security import get_current_admin
from app.models.schemas import UserSettings
from app.storage.file_storage import FileStorage
from app.core.config import settings
from app.core.rate_limit import limiter

router = APIRouter()

def get_file_storage() -> FileStorage:
    return FileStorage()

@router.get("/settings", response_model=UserSettings)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
def get_settings_endpoint(
    request: Request,
    admin: str = Depends(get_current_admin),
    storage: FileStorage = Depends(get_file_storage),
) -> UserSettings:
    saved = storage.load_settings()
    if not saved:
        return UserSettings()
    return UserSettings(
        base=saved.get("base", "EUR"),
        symbols=saved.get("symbols", []),
    )

@router.put("/settings", response_model=UserSettings)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
def update_settings_endpoint(
    request: Request,
    payload: UserSettings,
    admin: str = Depends(get_current_admin),
    storage: FileStorage = Depends(get_file_storage),
) -> UserSettings:
    storage.save_settings({"base": payload.base, "symbols": payload.symbols})
    return payload