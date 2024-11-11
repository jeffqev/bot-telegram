import pytest
import typing
from datetime import timezone

from faker import Faker
from app.expenses.domain.entities import Expense


@pytest.fixture(name="expense_factory")
def fixture_expense_factory(faker: Faker) -> typing.Callable[..., Expense]:
    def _expense_factory(**kwarg: typing.Dict[str, typing.Any]) -> Expense:
        return Expense(
            **{
            "id": faker.unique.pyint(),
            "user_id": faker.unique.pyint(),
            "description": faker.text(),
            "amount": 10,
            "category": faker.word(),
            "added_at": faker.date_time(tzinfo=timezone.utc),
            **kwarg,
            }
        )

    return _expense_factory
