from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.deps import SessionDep, RefreshToken

from app.domain.authentication.entities import Token, TokenPlayload, RefreshTokenPayload
from app.application.auth_service import AuthService
from app.infrastructure.postgres.auth_repository import SQLAlchemyAuthRepository

router = APIRouter(tags=["login"])


def get_auth_service(db: SessionDep) -> AuthService:
    return AuthService(SQLAlchemyAuthRepository(db))


ServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/access-token")
def login_access_token(
    service: ServiceDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    user = service.verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect email or password"
        )
    access_payload = TokenPlayload(sub=str(user.user_code), sv=user.session_version)
    access_token = service.get_token(access_payload)

    refresh_payload = RefreshTokenPayload(sub=str(user.user_code))
    refresh_token = service.get_refresh_token(refresh_payload)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return Token(access_token=access_token)


@router.post("/refresh", response_model=Token)
def refresh_access_token(service: ServiceDep, response: Response, user: RefreshToken):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token not found"
        )

    access_payload = TokenPlayload(sub=str(user.user_code), sv=user.session_version)
    access_token = service.get_token(access_payload)

    refresh_payload = RefreshTokenPayload(sub=str(user.user_code))
    refresh_token = service.get_refresh_token(refresh_payload)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return Token(access_token=access_token)
