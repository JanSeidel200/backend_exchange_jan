from fastapi import APIRouter, HTTPException, Request, Response, status

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import (
    COOKIE_NAME,
    create_access_token,
    verify_admin_credentials,
)
from app.models.schemas import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
@limiter.limit(f"{settings.auth_rate_limit_per_minute}/minute")
def login(payload: LoginRequest, response: Response, request: Request) -> LoginResponse:
    if not verify_admin_credentials(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(payload.username)
    is_production = settings.environment != "local"
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=is_production,
        samesite="none" if is_production else "lax",
        max_age=settings.jwt_expire_minutes * 60,
    )
    return LoginResponse(username=payload.username, message="Logged in", access_token=token,)

@router.post("/logout")
@limiter.limit(f"{settings.auth_rate_limit_per_minute}/minute")
def logout(request: Request, response: Response) -> dict[str, str]:
    response.delete_cookie(COOKIE_NAME)
    return {"message": "Logged out"}