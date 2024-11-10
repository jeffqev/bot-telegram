import http

from fastapi.testclient import TestClient
from faker import Faker

from app.expenses.cases.analyze_expense import (
    AnalyzeExpenseRequest,
    AnalyzeExpenseResponse,
)


class TestAnalyzeExpenseEndpoint:
    def test_analyze_expense_response_http_ok_status(
        self, api_client: TestClient, faker: Faker
    ):
        fake_id = str(faker.uuid4())
        fake_text = faker.text()
        request = AnalyzeExpenseRequest(user_id=fake_id, text=fake_text)
        expected_response = AnalyzeExpenseResponse(
            response=[
                AnalyzeExpenseResponse.Expense(
                    description="test", amount=10, category="test"
                )
            ]
        )

        response = api_client.post("/analyze_expense", json=request.model_dump())

        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == expected_response.model_dump()
