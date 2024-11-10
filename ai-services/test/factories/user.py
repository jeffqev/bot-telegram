import pytest
import typing

from faker import Faker
from app.expenses.domain.entities import User


@pytest.fixture(name="user_factory")
def fixture_user_factory(faker: Faker) -> typing.Callable[..., User]:
    def _user_factory(**kwarg: typing.Dict[str, typing.Any]) -> User:
        return User(
            **{
                "id": faker.unique.pyint(),
                "external_id": str(faker.uuid4()),
                **kwarg,
            }
        )

    return _user_factory
