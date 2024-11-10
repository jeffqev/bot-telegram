import pytest
from faker import Faker

from fastapi.testclient import TestClient
from app.entrypoints.http import app
from .factories import fixture_user_factory, fixture_expense_factory


@pytest.fixture(name="api_client")
def fixture_api_client() -> TestClient:
    client = TestClient(app)
    return client


@pytest.fixture(name="faker")
def fixture_faker():
    return Faker()
