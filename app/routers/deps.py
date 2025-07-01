from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import SessionLocal, API_V1_STR, SECRET, ALGORITHM
from app.domain.user.entities import User
from app.domain.authentication.entities import TokenPlayload, RefreshTokenPayload
from app.infrastructure.postgres.user_repository import SQLAlchemyUserRepository
from app.application.user_service import UserService

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/login/access-token")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_user_service(db: SessionDep) -> UserService:
    return UserService(SQLAlchemyUserRepository(db))


def get_current_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    token: TokenDep,
) -> User:
    try:
        paylaod = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        token_data = TokenPlayload(**paylaod)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_service.get_user_by_code(token_data.sub) # type: ignore
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.session_version != token_data.sv:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid session",
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def verify_refresh_token(
    user_service: Annotated[UserService, Depends(get_user_service)],
    refresh_token: str = Cookie(None),
) -> User:
    try:
        paylaod = jwt.decode(refresh_token, SECRET, algorithms=[ALGORITHM])
        token_data = RefreshTokenPayload(**paylaod)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = user_service.get_user_by_code(token_data.sub) # type: ignore
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


RefreshToken = Annotated[User, Depends(verify_refresh_token)]
