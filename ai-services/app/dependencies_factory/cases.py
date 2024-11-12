from ..expenses import cases
from . import repositories


async def analyze_expense_use_case(session) -> cases.AnalyzeExpenseCase:
    return cases.AnalyzeExpenseCase(
        expenses_repository=repositories.expenses_repository(session=session),
        user_repository=repositories.user_repository(session=session),
    )


async def add_user_use_case(session) -> cases.AddUserUseCase:
    return cases.AddUserUseCase(
        user_repository=repositories.user_repository(session=session),
    )
