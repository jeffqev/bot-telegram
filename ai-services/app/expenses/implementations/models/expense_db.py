import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.config.db import Base
from app.expenses.domain.entities import Expense
from .user_db import UserDB


class ExpenseDB(Base):
    __tablename__ = "expenses"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    description = sa.Column(sa.String, nullable=False)
    amount = sa.Column(sa.Numeric(precision=10, scale=2), nullable=False)
    category = sa.Column(sa.String, nullable=False)
    added_at = sa.Column(
        sa.DateTime(timezone=True), nullable=False
    )

    user = relationship(UserDB, foreign_keys=[user_id])

    def to_domain(self) -> Expense:
        return Expense(
            id=self.id,
            amount=self.amount,
            description=self.description,
            added_at=self.added_at,
            category=self.category,
            user_id=self.user_id,
        )
