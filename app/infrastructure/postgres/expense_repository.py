from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.ports.expense_respository import ExpenseRespository
from app.infrastructure.postgres.sqlalchemy_models import (
    ExpenseCategoryModel,
    ExpenseModel,
    UserCategory,
    UserModel,
)
from app.domain.expense.entities import (
    ExpenseCategory,
    Expense,
    ExpenseCategoryIn,
    ExpenseInDb,
    ExpenseCategoryUpdated,
    ExpenseUpdated,
)


class SQLAlchemyExpenseRepository(ExpenseRespository):
    def __init__(self, db: Session):
        self.db = db

    def find_categories_user(self, user_id: int) -> list[ExpenseCategory] | None:
        stmt = (
            select(UserCategory, ExpenseCategoryModel)
            .join(ExpenseCategoryModel)
            .where(UserCategory.user_id == user_id)
        )
        data = self.db.execute(stmt).all()
        if not data:
            return None
        categories = []
        for user_category, category in data:
            categories.append(ExpenseCategory.model_validate(category))
        return categories

    def find_expense_by_id(self, expense_id: int) -> Expense | None:
        stmt = select(ExpenseModel).where(ExpenseModel.expense_id == expense_id)
        data = self.db.execute(stmt).scalar_one_or_none()
        if not data:
            return None
        return Expense.model_validate(data)

    def find_expenses_by_range_date(
        self, start_date: date, end_date: date, user_id: int
    ) -> list[Expense] | None:
        stmt = (
            select(ExpenseModel, ExpenseCategoryModel.category_name)
            .join(ExpenseCategoryModel)
            .where(ExpenseModel.expense_date.between(start_date, end_date))
            .where(ExpenseModel.user_id == user_id)
        )
        result = self.db.execute(stmt).all()
        if not result:
            return None
        expenses = []
        for expense_model, category_name in result:
            expense_aux = Expense.model_validate(expense_model)
            expense_aux.category_name = category_name
            expenses.append(expense_aux)
        return expenses

    def save_category(self, category: ExpenseCategoryIn) -> ExpenseCategory | None:
        category_db = ExpenseCategoryModel(**category.model_dump())
        self.db.add(category_db)
        self.db.commit()
        self.db.refresh(category_db)
        return ExpenseCategory.model_validate(category_db)

    def save_expense(self, expense: ExpenseInDb) -> Expense | None:
        expense_db = ExpenseModel(**expense.model_dump())
        self.db.add(expense_db)
        self.db.commit()
        self.db.refresh(expense_db)
        return Expense.model_validate(expense_db)

    def update_category(
        self, category: ExpenseCategoryUpdated
    ) -> ExpenseCategory | None:
        stmt = select(ExpenseCategoryModel).where(
            ExpenseCategoryModel.category_id == category.category_id
        )
        category_db = self.db.execute(stmt).scalar_one_or_none()
        if not category_db:
            return None
        category_db.category_name = category.category_name  # type: ignore
        self.db.commit()
        self.db.refresh(category_db)
        return ExpenseCategory.model_validate(category_db)

    def update_expense(self, expense: ExpenseUpdated) -> Expense | None:
        stmt = select(ExpenseModel).where(ExpenseModel.expense_id == expense.expense_id)
        expense_db = self.db.execute(stmt).scalar_one_or_none()
        if not expense_db:
            return None
        expense_db.amount = expense.amount  # type: ignore
        expense_db.expense_date = expense.expense_date  # type: ignore
        expense_db.category_id = expense.category_id  # type: ignore
        expense_db.description = expense.description  # type: ignore
        self.db.commit()
        self.db.refresh(expense_db)
        return Expense.model_validate(expense_db)

    def delete_expense(self, expense_id: int) -> bool:
        stmt = select(ExpenseModel).where(ExpenseModel.expense_id == expense_id)
        expense_db = self.db.execute(stmt).scalar_one_or_none()
        if not expense_db:
            return False
        self.db.delete(expense_db)
        self.db.commit()

        stmt_check = select(ExpenseModel).where(ExpenseModel.expense_id == expense_id)
        expense_check = self.db.execute(stmt_check).scalar_one_or_none()
        if expense_check:
            return False
        return True
