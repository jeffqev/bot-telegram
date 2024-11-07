from fastapi.testclient import TestClient


def test_health_check_returns_status_ok(api_client: TestClient):
    response = api_client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}