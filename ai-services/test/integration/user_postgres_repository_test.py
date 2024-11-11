import typing
import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.expenses.implementations import UserPostgresRepository
from app.expenses.domain.entities import User


@pytest.mark.asyncio
class TestUserPostgresRepository:
    async def test_get_by_external_id_return_the_correct_user(
        self, db_session: AsyncSession,
        save_fake_user: typing.Callable[..., User],
        clear_tables
    ):
        fake_stored_user = await save_fake_user(external_id="123")
        repository = UserPostgresRepository(db_session)

        result = await repository.get_by_external_id(fake_stored_user.external_id)

        assert fake_stored_user.external_id == result.external_id
        assert fake_stored_user.id == result.id

    async def test_get_by_external_id_returns_none_when_user_not_found(
        self, db_session: AsyncSession
    ):
        external_id = "123"
        repository = UserPostgresRepository(db_session)

        result = await repository.get_by_external_id(external_id)

        assert result is None
