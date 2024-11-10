import pydantic
from datetime import datetime


class ExpenseCreation(pydantic.BaseModel):
    user_id: int
    description: str
    amount: float
    category: str


class Expense(pydantic.BaseModel):
    id: int
    user_id: int
    description: str
    amount: float
    category: str
    added_at: datetime


class AnalyzedExpense(pydantic.BaseModel):
    description: str
    amount: float
    category: str
