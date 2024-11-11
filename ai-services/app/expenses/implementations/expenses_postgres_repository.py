import json
import typing
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.expenses.domain.repositories import ExpensesRepository, GenerativeAIRepository
from app.expenses.domain.entities import Expense, ExpenseCreation, AnalyzedExpense
from app.expenses.implementations.models import ExpenseDB
from app.config.template import analyze_from_text_template
from logging import getLogger

logger = getLogger(__name__)


class ExpensesPostgresRepository(ExpensesRepository):
    def __init__(
        self, session: AsyncSession, generative_ai_repository: GenerativeAIRepository
    ):
        self.session = session
        self.generative_ai_repository = generative_ai_repository

    async def bulk_insert(
        self,
        expenses: typing.List[ExpenseCreation],
    ) -> typing.List[Expense]:
        try:
            expenses_db = [
                ExpenseDB(
                    **expense.model_dump(),
                    added_at=datetime.now(timezone.utc),
                )
                for expense in expenses
            ]
            self.session.add_all(expenses_db)
            await self.session.commit()
            return [expense.to_domain() for expense in expenses_db]
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def analyze_from_text(self, text: str) -> typing.List[AnalyzedExpense]:
        try:
            answer = await self.generative_ai_repository.ask(
                prompt=text, template=analyze_from_text_template
            )
            data = json.loads(answer)

            if data.get("error"):
                logger.error(f"Error while analyzing the text: {data.get('error')}")
                return None

            return [
                AnalyzedExpense(
                    description=data.get("concept"),
                    amount=round(float(data.get("amount")), 2),
                    category=data.get("category"),
                )
            ]

        except json.JSONDecodeError as e:
            logger.error(f"Error while decoding the response: {e}")
            return None

        except Exception as e:
            logger.error(f"Error while analyzing the text: {e}")
            return None
