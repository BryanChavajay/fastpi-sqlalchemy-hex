from uuid import UUID
from abc import ABC, abstractmethod

from app.domain.user.entities import UserInDB, UpdatedUserDB, User


class UserRepository(ABC):
    @abstractmethod
    def find_by_code(self, user_code: UUID) -> User | None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def find_by_username(self, user_code: str) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, user_code: str) -> User | None:
        pass

    @abstractmethod
    def save(self, user: UserInDB, categories: list[str]) -> User:
        pass

    @abstractmethod
    def update(self, user: UpdatedUserDB) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_code: UUID) -> bool:
        pass
