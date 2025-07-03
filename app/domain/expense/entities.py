from decimal import Decimal
from datetime import date

from pydantic import BaseModel, Field, ConfigDict


class BaseExpenseCategory(BaseModel):
    category_name: str = Field(min_length=1, max_length=50)


class ExpenseCategory(BaseExpenseCategory):
    category_id: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class ExpenseBase(BaseModel):
    category_id: int = Field(gt=0)
    description: str = Field(max_length=250)
    amount: Decimal = Field(max_digits=18, decimal_places=2)
    expense_date: date


class Expense(ExpenseBase):
    expense_id: int = Field(gt=0)
    category_name: str | None = Field(default=None)
    user_id: int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


# Inside
class ExpenseCategoryIn(BaseExpenseCategory):
    pass


class ExpenseIn(ExpenseBase):
    pass


class ExpenseInDb(ExpenseIn):
    user_id: int = Field(gt=0)


# Update
class ExpenseUpdated(ExpenseBase):
    expense_id: int = Field(gt=0)


class ExpenseCategoryUpdated(BaseExpenseCategory):
    category_id: int = Field(gt=0)


# Public
class MinPublicExpense(ExpenseBase):
    expense_id: int = Field(gt=0)


class PublicExpense(ExpenseBase):
    expense_id: int = Field(gt=0)
    category_name: str
