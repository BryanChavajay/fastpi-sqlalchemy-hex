from datetime import date

from fastapi import HTTPException, status

from app.ports.expense_respository import ExpenseRespository
from app.domain.expense.entities import (
    ExpenseInDb,
    Expense,
    ExpenseUpdated,
    ExpenseCategoryIn,
    ExpenseCategoryUpdated,
    ExpenseCategory,
)
from app.utils import obtener_fecha_actual


class ExpenseService:
    def __init__(self, expense_repository: ExpenseRespository):
        self.expense_repository = expense_repository

    def get_categories_user(self, user_id: int) -> list[ExpenseCategory]:
        categories = self.expense_repository.find_categories_user(user_id)
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categories not found"
            )
        return categories

    def get_expense_by_id(self, expense_id: int, user_id: int) -> Expense:
        expense = self.expense_repository.find_expense_by_id(expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
            )
        if expense.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
            )
        return expense

    def get_expense_by_range(
        self, start_date: date | None, end_date: date | None, user_id: int
    ) -> list[Expense]:
        start_date = start_date or obtener_fecha_actual()
        end_date = end_date or obtener_fecha_actual()
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong dates"
            )
        expenses = self.expense_repository.find_expenses_by_range_date(
            start_date, end_date, user_id
        )
        if not expenses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expenses not found"
            )
        return expenses

    def create_expense(self, expense: ExpenseInDb) -> Expense:
        categories = self.expense_repository.find_categories_user(expense.user_id)
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Does not have categories",
            )
        exist_category = False
        for category in categories:
            if category.category_id == expense.category_id:
                exist_category = True
        if not exist_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        new_expense = self.expense_repository.save_expense(expense)
        if not new_expense:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Expense could not be registered",
            )
        return new_expense

    def create_category(self, category: ExpenseCategoryIn) -> ExpenseCategory:
        new_category = self.expense_repository.save_category(category)
        if not new_category:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Category could not be registered",
            )
        return new_category

    def update_expense(self, expense: ExpenseUpdated, user_id: int) -> Expense:
        categories = self.expense_repository.find_categories_user(user_id)
        if not categories:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
            )
        exist_category = False
        for category in categories:
            if category.category_id == expense.category_id:
                exist_category = True
        if not exist_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
            )
        new_expense = self.expense_repository.update_expense(expense)
        if not new_expense:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Category could not be updated",
            )
        return new_expense

    def update_category(self, category: ExpenseCategoryUpdated) -> ExpenseCategory:
        new_category = self.expense_repository.update_category(category)
        if not new_category:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Category could not be updated",
            )
        return new_category

    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        expense = self.expense_repository.find_expense_by_id(expense_id)
        if not expense:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
            )
        if expense.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found"
            )
        expense_deleted = self.expense_repository.delete_expense(expense_id)
        if not expense_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Expense could not be deleted",
            )
        return expense_deleted
