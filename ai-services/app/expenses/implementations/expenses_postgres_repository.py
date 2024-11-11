import typing
from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.expenses.domain.repositories import ExpensesRepository
from app.expenses.domain.entities import Expense, ExpenseCreation
from app.expenses.implementations.models import ExpenseDB


class ExpensesPostgresRepository(ExpensesRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_insert(
        self,
        expenses: typing.List[ExpenseCreation],
    ) -> typing.List[Expense]:
        try:
            expenses_db = [
                ExpenseDB(**expense.model_dump(), added_at=datetime.now(timezone.utc))
                for expense in expenses
            ]
            self.session.add_all(expenses_db)
            await self.session.commit()
            return [expense.to_domain() for expense in expenses_db]
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def analyze_from_text(self, text: str) -> typing.List[Expense]:
        return []
