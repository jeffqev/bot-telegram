import pytest
import typing

import sqlalchemy as sa
from faker import Faker
from app.expenses.domain.entities import User
from sqlalchemy.ext.asyncio import AsyncSession


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


@pytest.fixture(name="save_fake_user")
def fixture_save_user(
    user_factory: typing.Callable[..., User], db_session: AsyncSession
) -> typing.Callable[..., User]:
    async def _save_user(**kwargs: typing.Dict[str, typing.Any]) -> User:
        user = user_factory(**kwargs)
        query = sa.text("INSERT INTO users (id, telegram_id) VALUES (:id, :telegram_id)")
        await db_session.execute(
            query, {"id": user.id, "telegram_id": user.external_id}
        )
        await db_session.commit()
        return user

    return _save_user
