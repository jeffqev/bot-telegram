from .request import AnalyzeExpenseRequest
from .response import AnalyzeExpenseResponse
from ...domain.repositories import ExpensesRepository, UserRepository
from ...domain.exceptions import UserNotFoundException, NoExpensesFoundException
from ...domain.entities import ExpenseCreation


class AnalyzeExpenseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        expenses_repository: ExpensesRepository,
    ):
        self.user_repository = user_repository
        self.expenses_repository = expenses_repository

    async def __call__(self, request: AnalyzeExpenseRequest) -> AnalyzeExpenseResponse:
        found_user = await self.user_repository.get_by_external_id(request.user_id)

        if not found_user:
            raise UserNotFoundException(
                f"User with id {request.user_id} not authorized"
            )

        expenses = await self.expenses_repository.analyze_from_text(request.text)

        if not expenses:
            raise NoExpensesFoundException("Error while analyzing the text")

        expenses_to_insert = [
            ExpenseCreation(
                user_id=found_user.id,
                description=expense.description,
                amount=expense.amount,
                category=expense.category,
            )
            for expense in expenses
        ]

        await self.expenses_repository.bulk_insert(expenses=expenses_to_insert)

        return AnalyzeExpenseResponse(
            response=[
                AnalyzeExpenseResponse.Expense(**expense.model_dump())
                for expense in expenses
            ]
        )
