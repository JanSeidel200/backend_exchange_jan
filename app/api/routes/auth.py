from fastapi import APIRouter, HTTPException, Response, status

from app.core.config import settings
from app.core.security import (
    COOKIE_NAME,
    create_access_token,
    verify_admin_credentials,
)
from app.models.schemas import LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, response: Response) -> LoginResponse:
    if not verify_admin_credentials(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(payload.username)
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.environment != "local",
        samesite="lax",
        max_age=settings.jwt_expire_minutes * 60,
    )
    return LoginResponse(username=payload.username, message="Logged in")

@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie(COOKIE_NAME)
    return {"message": "Logged out"}