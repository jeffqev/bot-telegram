import typing
import pytest
from faker import Faker

from app.expenses.cases import (
    AnalyzeExpenseRequest,
    AnalyzeExpenseCase,
    AnalyzeExpenseResponse,
)
from app.expenses.domain.exceptions import (
    UserNotFoundException,
    NoExpensesFoundException,
)
from app.expenses.domain.entities import User, ExpenseCreation, AnalyzedExpense
from pytest_mock import MockerFixture


@pytest.mark.asyncio
class TestAnalyzeExpenseCase:
    async def test_analyze_expense_case_returns_expenses_analyzed(
        self,
        mocker: MockerFixture,
        faker: Faker,
        user_factory: typing.Callable[..., User],
    ):
        user_id = str(faker.unique.pyint())
        fake_text = faker.text()
        fake_user = user_factory(external_id=user_id)
        fake_analyzed_expense = [
            AnalyzedExpense(description=faker.text(), category=faker.word(), amount=i)
            for i in range(faker.random_int(min=1, max=10))
        ]
        request = AnalyzeExpenseRequest(user_id=user_id, text=fake_text)
        user_repository_mock = mocker.Mock(
            get_by_external_id=mocker.AsyncMock(return_value=fake_user)
        )
        expenses_repository_mock = mocker.Mock(
            analyze_from_text=mocker.AsyncMock(return_value=fake_analyzed_expense),
            bulk_insert=mocker.AsyncMock(),
        )
        analyze_expense_case = AnalyzeExpenseCase(
            user_repository=user_repository_mock,
            expenses_repository=expenses_repository_mock,
        )

        response = await analyze_expense_case(request)

        user_repository_mock.get_by_external_id.assert_called_once_with(user_id)
        expenses_repository_mock.analyze_from_text.assert_called_once_with(fake_text)
        expenses_repository_mock.bulk_insert.assert_called_once_with(
            expenses=[
                ExpenseCreation(
                    user_id=fake_user.id,
                    description=expense.description,
                    amount=expense.amount,
                    category=expense.category,
                )
                for expense in fake_analyzed_expense
            ]
        )
        assert response == AnalyzeExpenseResponse(
            response=[
                AnalyzeExpenseResponse.Expense(**expense.model_dump())
                for expense in fake_analyzed_expense
            ]
        )

    async def test_analyze_expense_case_raises_user_not_found_exception(
        self, mocker: MockerFixture, faker: Faker
    ):
        user_id = str(faker.unique.pyint())
        fake_text = faker.text()
        request = AnalyzeExpenseRequest(user_id=user_id, text=fake_text)
        user_repository_mock = mocker.Mock(get_by_external_id=mocker.AsyncMock(return_value=None))
        analyze_expense_case = AnalyzeExpenseCase(
            user_repository=user_repository_mock,
            expenses_repository=mocker.Mock(),
        )
        expected_exception = f"User with id {user_id} not authorized"

        with pytest.raises(UserNotFoundException) as exc:
            await analyze_expense_case(request)

        assert str(exc.value) == expected_exception

    async def test_analyze_expense_case_raises_no_expenses_found_exception(
        self,
        mocker: MockerFixture,
        faker: Faker,
        user_factory: typing.Callable[..., User],
    ):
        user_id = str(faker.unique.pyint())
        fake_text = faker.text()
        fake_user = user_factory(external_id=user_id)
        request = AnalyzeExpenseRequest(user_id=user_id, text=fake_text)
        user_repository_mock = mocker.Mock(
            get_by_external_id=mocker.AsyncMock(return_value=fake_user)
        )
        expenses_repository_mock = mocker.Mock(
            analyze_from_text=mocker.AsyncMock(return_value=[]),
        )
        analyze_expense_case = AnalyzeExpenseCase(
            user_repository=user_repository_mock,
            expenses_repository=expenses_repository_mock,
        )
        expected_exception = "No expenses found in the text"

        with pytest.raises(NoExpensesFoundException) as exc:
            await analyze_expense_case(request)

        assert str(exc.value) == expected_exception
