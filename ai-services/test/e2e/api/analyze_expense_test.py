import typing
import http
import pytest
import json

from fastapi.testclient import TestClient
from faker import Faker

from app.expenses.cases.analyze_expense import (
    AnalyzeExpenseRequest,
    AnalyzeExpenseResponse,
)
from app.expenses.domain.entities import User
from pytest_mock import MockerFixture
from app.config.template import analyze_from_text_template


@pytest.mark.asyncio
class TestAnalyzeExpenseEndpoint:
    async def test_analyze_expense_response_http_ok_status(
        self,
        mocker: MockerFixture,
        api_client: TestClient,
        faker: Faker,
        save_fake_user: typing.Callable[..., User],
        clear_tables,
    ):
        fake_id = str(faker.uuid4())
        await save_fake_user(external_id=fake_id)
        fake_open_ai_response = {"concept": "test", "amount": 10, "category": "test"}
        fake_text = faker.text()
        request = AnalyzeExpenseRequest(user_id=fake_id, text=fake_text)

        mocked_call_to_openai = mocker.patch(
            "app.expenses.implementations.generative_ai_langchain_repository.GenerativeAILangchainRepository.ask",  # noqa: E501
            return_value=json.dumps(fake_open_ai_response),
        )

        expected_response = AnalyzeExpenseResponse(
            response=[
                AnalyzeExpenseResponse.Expense(
                    description=fake_open_ai_response["concept"],
                    amount=fake_open_ai_response["amount"],
                    category=fake_open_ai_response["category"],
                )
            ]
        )

        response = api_client.post("/analyze_expense", json=request.model_dump())

        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == expected_response.model_dump()
        mocked_call_to_openai.assert_called_once_with(
            prompt=fake_text, template=analyze_from_text_template
        )
