import typing

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.expenses.domain.repositories import UserRepository
from app.expenses.implementations.models import UserDB
from app.expenses.domain.entities import User, UserCreation


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

    async def bulk_insert(self, users: typing.List[UserCreation]) -> typing.List[User]:
        try:
            users_db = [UserDB(telegram_id=user.external_id) for user in users]
            self.session.add_all(users_db)
            await self.session.commit()
            return [user.to_domain() for user in users_db]
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
