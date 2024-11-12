import asyncio
import pytest
import sqlalchemy as sa
from faker import Faker

from typer.testing import CliRunner
from fastapi.testclient import TestClient
from app.entrypoints.http import app
from app.config.db import create_session_maker
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession

from .factories import fixture_user_factory, fixture_expense_factory, fixture_save_user


@pytest.fixture(name="api_client")
def fixture_api_client() -> TestClient:
    client = TestClient(app)
    return client

@pytest.fixture(name="cli_runner")
def fixture_cli_runner(mocker: MockerFixture) -> CliRunner:
    mocker.patch.dict(
        "os.environ",
        {
            "DB_HOSTNAME": "db-test",
            "DB_NAME": "bot-ai",
            "DB_PASSWORD": "postgres",
            "DB_USER": "postgres",
            "DB_PORT": "5432",
        },
    )
    return CliRunner()


@pytest.fixture(name="faker")
def fixture_faker():
    return Faker()


@pytest.fixture(scope="function")
def db_session(mocker: MockerFixture):
    mocker.patch.dict(
        "os.environ",
        {
            "DB_HOSTNAME": "db-test",
            "DB_NAME": "bot-ai",
            "DB_PASSWORD": "postgres",
            "DB_USER": "postgres",
            "DB_PORT": "5432",
        },
    )

    session_maker = create_session_maker()
    session = session_maker()

    try:
        yield session
    finally:
        asyncio.run(session.close())


@pytest.fixture(name="clear_tables")
def _clear_tables_fixture(db_session: AsyncSession):
    yield
    asyncio.run(db_session.execute(sa.text("DELETE FROM expenses")))
    asyncio.run(db_session.execute(sa.text("DELETE FROM users")))
    asyncio.run(db_session.commit())
