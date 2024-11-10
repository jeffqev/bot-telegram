import typing
import pydantic


class AnalyzeExpenseResponse(pydantic.BaseModel):
    class Expense(pydantic.BaseModel):
        description: str
        amount: float
        category: str

    response: typing.List[Expense]
