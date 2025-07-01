from uuid import UUID
from abc import ABC, abstractmethod

from app.domain.authentication.entities import User


class AuthRepository(ABC):
    @abstractmethod
    def find_by_code(self, user_code: UUID) -> User | None:
        pass

    @abstractmethod
    def find_by_username(self, user_code: str) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, user_code: str) -> User | None:
        pass