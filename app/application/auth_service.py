from uuid import UUID
from datetime import timedelta

from fastapi import HTTPException, status

from app.domain.authentication.entities import User, TokenPlayload, RefreshTokenPayload
from app.ports.auth_repository import AuthRepository
from app.utils import verify_password, create_access_token
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:
    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def verify_user(self, username: str, password: str) -> User:
        user = (
            self.auth_repository.find_by_email(username)
            if "@" in username
            else self.auth_repository.find_by_username(username)
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )
        if not verify_password(hashed_password=user.password, plain_password=password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )
        return user

    def get_token(self, token_payload: TokenPlayload) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(token_payload.model_dump(), access_token_expires)

    def get_refresh_token(self, refresh_payload: RefreshTokenPayload) -> str:
        refresh_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(refresh_payload.model_dump(), refresh_token_expires)

    def get_user_by_sub(self, sub: UUID) -> User:
        user = self.auth_repository.find_by_code(sub)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
