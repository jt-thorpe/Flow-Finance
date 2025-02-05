import uuid
from typing import Dict, Final

from core.extensions import db
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

GEN_RANDOM_UUID: Final[str] = "gen_random_uuid()"


class User(db.Model):
    """Models a user account.

    Attributes:
        id: The UUID of the user.
        email: The email address of the user.
        password: The hashed password of the user.
        alias: The alias of the user.

    Relationships:
        incomes: The user's financial incomes.
        expenses: The user's financial expenses.
        budgets: The user's budgets.
    """
    __tablename__ = "user_account"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    email: str = db.Column(db.String(100),
                           unique=True,
                           nullable=False)
    password: str = db.Column(db.String(100),
                              nullable=False)
    alias: str = db.Column(db.String(30),
                           nullable=False)

    incomes = db.relationship("Income", back_populates="user")
    expenses = db.relationship("Expense", back_populates="user")
    budgets = db.relationship("Budget", back_populates="user")

    def to_dict(self) -> Dict:
        """Returns the User object and it's related data in a JSON serialisable format."""
        return {
            "meta": {"id": str(self.id), "alias": self.alias},
            "incomes": [income.to_dict() for income in self.incomes],
            "expenses": [expense.to_dict() for expense in self.expenses],
            "budgets": [budget.to_dict() for budget in self.budgets],
        }
