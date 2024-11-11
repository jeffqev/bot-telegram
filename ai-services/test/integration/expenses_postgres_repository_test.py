import typing
import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.expenses.implementations import ExpensesPostgresRepository
from app.expenses.domain.entities import Expense, ExpenseCreation, User


@pytest.mark.asyncio
class TestExpensesPostgresRepository:
    async def test_bulk_insert_returns_the_correct_expenses(
        self,
        db_session: AsyncSession,
        expense_factory: typing.Callable[..., Expense],
        save_fake_user: typing.Callable[..., User],
        clear_tables,
    ):
        user = await save_fake_user()
        expected_expenses = [
            ExpenseCreation(**expense_factory(user_id=user.id).model_dump())
            for _i in range(5)
        ]
        repository = ExpensesPostgresRepository(session=db_session, generative_ai_repository=None)

        result = await repository.bulk_insert(expected_expenses)

        assert len(result) == 5
        for result, expected in zip(result, expected_expenses):
            assert expected.user_id == result.user_id
            assert expected.description == result.description
            assert expected.amount == result.amount
            assert expected.category == result.category
