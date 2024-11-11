import pydantic
from datetime import datetime
import decimal

class ExpenseCreation(pydantic.BaseModel):
    user_id: int
    description: str
    amount: decimal.Decimal
    category: str


class Expense(pydantic.BaseModel):
    id: int
    user_id: int
    description: str
    amount: decimal.Decimal
    category: str
    added_at: datetime


class AnalyzedExpense(pydantic.BaseModel):
    description: str
    amount: decimal.Decimal
    category: str
