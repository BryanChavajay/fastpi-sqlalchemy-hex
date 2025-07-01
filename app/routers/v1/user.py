from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.deps import CurrentUser, SessionDep
from app.domain.user.entities import PublicMinUser, UserIn, PublicUser
from app.application.user_service import UserService
from app.infrastructure.postgres.user_repository import SQLAlchemyUserRepository


def get_user_service(db: SessionDep) -> UserService:
    return UserService(SQLAlchemyUserRepository(db))


ServiceDep = Annotated[UserService, Depends(get_user_service)]

router = APIRouter(tags=["user"])


@router.post("/me", response_model=PublicMinUser)
def who_am_i(user: CurrentUser) -> Any:
    return user


@router.post("/", response_model=PublicUser)
def register_user(user: UserIn, service: ServiceDep):
    new_user = service.create_user(user)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User dont created",
        )
    return new_user
