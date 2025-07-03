from typing import Any, Annotated
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path

from app.routers.deps import CurrentUser, SessionDep
from app.domain.expense.entities import (
    ExpenseIn,
    PublicExpense,
    MinPublicExpense,
    ExpenseCategory,
    ExpenseInDb,
    ExpenseUpdated,
    ExpenseCategoryUpdated,
)
from app.application.expense_service import ExpenseService
from app.infrastructure.postgres.expense_repository import SQLAlchemyExpenseRepository


def get_expense_service(db: SessionDep) -> ExpenseService:
    return ExpenseService(SQLAlchemyExpenseRepository(db))


ServiceDep = Annotated[ExpenseService, Depends(get_expense_service)]


router = APIRouter(tags=["expense"])


@router.post("/", response_model=MinPublicExpense)
def register_expense(
    service: ServiceDep, current_user: CurrentUser, expense: ExpenseIn
):
    expense_db = ExpenseInDb(**expense.model_dump(), user_id=current_user.id)
    new_expense = service.create_expense(expense_db)
    return new_expense


@router.get("/", response_model=list[PublicExpense])
def get_expenses(
    service: ServiceDep,
    current_user: CurrentUser,
    start_date: date | None = Query(alias="start-date", default=None),
    end_date: date | None = Query(alias="end-date", default=None),
):
    expenses = service.get_expense_by_range(start_date, end_date, current_user.id)
    return expenses


@router.get("/categories", response_model=list[ExpenseCategory])
def get_categories(service: ServiceDep, current_user: CurrentUser):
    print("Entro a la ruta")
    categories = service.get_categories_user(current_user.id)
    return categories


@router.get("/{expense_id}", response_model=MinPublicExpense)
def get_expense(
    service: ServiceDep, current_user: CurrentUser, expense_id: int = Path(gt=0)
):
    expense = service.get_expense_by_id(expense_id, current_user.id)
    return expense


@router.put("/", response_model=MinPublicExpense)
def update_expense(
    service: ServiceDep, current_user: CurrentUser, expense: ExpenseUpdated
):
    new_expense = service.update_expense(expense, current_user.id)
    return new_expense


@router.put("/category", response_model=ExpenseCategory)
def update_category(
    service: ServiceDep, current_user: CurrentUser, category: ExpenseCategoryUpdated
):
    new_category = service.update_category(category)
    return new_category


@router.delete("/{expense_id}")
def delete_expense(
    service: ServiceDep, current_user: CurrentUser, expense_id: int = Path(gt=0)
):
    expense_deleted = service.delete_expense(expense_id, current_user.id)
    if not expense_deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error")
    else:
        return {"detail": "Expense deleted"}
