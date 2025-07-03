from abc import ABC, abstractmethod
from datetime import date

from app.domain.expense.entities import (
    ExpenseCategory,
    Expense,
    ExpenseCategoryIn,
    ExpenseInDb,
    ExpenseCategoryUpdated,
    ExpenseUpdated,
)


class ExpenseRespository(ABC):
    @abstractmethod
    def find_categories_user(self, user_id: int) -> list[ExpenseCategory] | None:
        pass

    @abstractmethod
    def find_expense_by_id(self, expense_id: int) -> Expense | None:
        pass

    @abstractmethod
    def find_expenses_by_range_date(
        self, start_date: date, end_date: date, user_id: int
    ) -> list[Expense] | None:
        pass

    @abstractmethod
    def save_category(self, category: ExpenseCategoryIn) -> ExpenseCategory | None:
        pass

    @abstractmethod
    def save_expense(self, expense: ExpenseInDb) -> Expense | None:
        pass

    @abstractmethod
    def update_category(
        self, category: ExpenseCategoryUpdated
    ) -> ExpenseCategory | None:
        pass

    @abstractmethod
    def update_expense(self, expense: ExpenseUpdated) -> Expense | None:
        pass

    @abstractmethod
    def delete_expense(self, expense_id: int) -> bool:
        pass
