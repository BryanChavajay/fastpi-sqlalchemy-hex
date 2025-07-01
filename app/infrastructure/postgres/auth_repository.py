from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ports.auth_repository import AuthRepository
from app.infrastructure.postgres.sqlalchemy_models import UserModel
from app.domain.authentication.entities import User


class SQLAlchemyAuthRepository(AuthRepository):
    def __init__(self, db: Session):
        self.db = db

    def find_by_code(self, user_code: UUID) -> User | None:
        stmt = select(UserModel).where(UserModel.user_code == user_code)
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