import pytest

from fastapi.testclient import TestClient
from app.entrypoints.http import app

@pytest.fixture(name="api_client")
def fixture_api_client() -> TestClient:
    client = TestClient(app)
    return client
