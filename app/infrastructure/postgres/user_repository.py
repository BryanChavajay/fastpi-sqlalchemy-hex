from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.ports.user_repository import UserRepository
from app.infrastructure.postgres.sqlalchemy_models import UserModel, ExpenseCategoryModel, UserCategory
from app.domain.user.entities import User, UserInDB, UpdatedUserDB


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def find_by_code(self, user_code: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.user_code == user_code)
        data = self.db.execute(stmt).scalar_one_or_none()
        if not data:
            return None
        return User.model_validate(data)

    def find_by_id(self, user_id: int) -> User | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        data = self.db.execute(stmt).scalar_one_or_none()
        if not data:
            return None
        return User.model_validate(data)

    def find_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        data = self.db.execute(stmt).scalar_one_or_none()
        if not data:
            return None
        return User.model_validate(data)

    def find_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        data = self.db.execute(stmt).scalar_one_or_none()
        if not data:
            return None
        return User.model_validate(data)

    def save(self, user: UserInDB, categories: list[str]) -> User:
        user_db = UserModel(**user.model_dump())
        self.db.add(user_db)
        self.db.flush()
        default_categories = [ExpenseCategoryModel(category_name=category) for category in categories]
        self.db.add_all(default_categories)
        self.db.flush()
        user_db.categories.extend(default_categories)
        self.db.commit()
        self.db.refresh(user_db)
        return User.model_validate(user_db)

    def update(self, user: UpdatedUserDB) -> User | None:
        stmt = select(UserModel).where(UserModel.user_code == user.user_code)
        user_db = self.db.execute(stmt).scalar_one_or_none()
        if not user_db:
            return None
        user_db.username = user.username # type: ignore
        user_db.email = user.email # type: ignore
        user_db.password = user.password # type: ignore
        user_db.session_version = user.session_version # type: ignore
        self.db.commit()
        self.db.refresh(user_db)
        return User.model_validate(user_db)

    def delete(self, user_code: UUID) -> bool:
        stmt = select(UserModel).where(UserModel.user_code == user_code)
        user = self.db.execute(stmt).scalar_one_or_none()
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()

        stmt_check = select(UserModel).where(UserModel.user_code == user_code)
        deleted_user = self.db.execute(stmt_check).scalar_one_or_none()
        if not deleted_user:
            return True
        return False
