import typing

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.expenses.domain.repositories import UserRepository
from app.expenses.implementations.models import UserDB
from app.expenses.domain.entities import User


class UserPostgresRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_external_id(self, external_id: str) -> typing.Optional[User]:
        try:
            user_query = await self.session.execute(
                select(UserDB).filter_by(telegram_id=external_id)
            )
            user = user_query.scalars().first()
            return user.to_domain() if user else None
        except SQLAlchemyError as e:
            raise e
