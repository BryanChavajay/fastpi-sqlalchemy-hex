from uuid import UUID

from fastapi import HTTPException, status

from app.ports.user_repository import UserRepository
from app.domain.user.entities import User, UserIn, UserInDB, UpdatedUser, UpdatedUserDB
from app.utils import get_password_hash


class UserService:
    def __init__(self, user_respository: UserRepository):
        self.user_repository = user_respository

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.find_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def get_user_by_code(self, user_id: UUID) -> User:
        user = self.user_repository.find_by_code(user_code=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    def create_user(self, user: UserIn) -> User:
        exist_username = self.user_repository.find_by_username(user.username)
        exist_email = self.user_repository.find_by_email(user.email)
        if exist_username or exist_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered",
            )
        hashed_password = get_password_hash(user.password)
        user_db = UserInDB(
            **user.model_dump(exclude={"password"}), password=hashed_password
        )
        default_categories = [
            "Comestibles",
            "Ocio",
            "Electrónica",
            "Utilidades",
            "Ropa",
            "Salud",
            "Otros",
        ]
        new_user = self.user_repository.save(user_db, default_categories)
        return new_user

    def update_user(self, user: UpdatedUser) -> User:
        old_data_user = self.user_repository.find_by_code(user.user_code)
        if not old_data_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        exist_username = self.user_repository.find_by_username(user.username)
        exist_email = self.user_repository.find_by_email(user.email)
        if exist_username or exist_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered",
            )

        hashed_password = ""
        new_data_user = UpdatedUserDB(
            **user.model_dump(),
            password=hashed_password,
            session_version=old_data_user.session_version + 1,
        )
        updated_user = self.user_repository.update(new_data_user)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User could not be updated",
            )
        return updated_user
