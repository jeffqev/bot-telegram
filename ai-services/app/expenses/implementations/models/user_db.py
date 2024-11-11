from sqlalchemy import Column, Integer, String
from app.config.db import Base
from app.expenses.domain.entities import User

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, nullable=False)

    def to_domain(self) -> User:
        return User(id=self.id, external_id=self.telegram_id)

