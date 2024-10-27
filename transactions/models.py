import uuid
from typing import Final, Optional

from sqlalchemy import Date, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from core.extensions import db
from transactions.enums import Frequency, TransactionCategory

GEN_RANDOM_UUID: Final[str] = "gen_random_uuid()"
USER_ACCOUNT_ID: Final[str] = "user_account.id"


class Income(db.Model):
    """Models a user's financial incomes.

    Attributes:
        id: The UUID of the income.
        user_id: The UUID of the user.
        category: The category of the income.
        date: The date of the income.
        frequency: The frequency of the income.
        amount: The amount of the income.
        description: A description of the income.

    Relationships:
        user: The user to whom the income belongs.
    """
    __tablename__ = "income"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey(USER_ACCOUNT_ID),
                                   nullable=False)
    category: TransactionCategory = db.Column(Enum(TransactionCategory),
                                              nullable=False)
    date: Date = db.Column(db.Date,
                           nullable=False)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=True)
    amount: int = db.Column(db.Integer,
                            nullable=False)
    description: Optional[str] = db.Column(String(100),
                                           nullable=True)

    user = db.relationship("User", back_populates="incomes")

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "category": self.category.name,
            "date": str(self.date),
            "frequency": self.frequency.name if self.frequency else None,
            "amount": self.amount,
            "description": self.description
        }


class Expense(db.Model):
    """Models a user's financial expenses.

    Attributes:
        id: The UUID of the expense.
        user_id: The UUID of the user.
        category: The category of the expense.
        date: The date of the expense.
        frequency: The frequency of the expense.
        amount: The amount of the expense.
        description: A description of the expense.

    Relationships:
        user: The user to whom the expense belongs.
    """
    __tablename__ = "expense"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey(USER_ACCOUNT_ID),
                                   nullable=False)
    category: TransactionCategory = db.Column(Enum(TransactionCategory),
                                              nullable=False)
    date: Date = db.Column(db.Date,
                           nullable=False)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=True)
    amount: int = db.Column(db.Integer,
                            nullable=False)

    description: Optional[str] = db.Column(String(100),
                                           nullable=True)

    user = db.relationship("User", back_populates="expenses")

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "category": self.category.name,
            "date": str(self.date),
            "frequency": self.frequency.name if self.frequency else None,
            "amount": self.amount,
            "description": self.description
        }


class Budget(db.Model):
    """Models a user's budget for a specific category.

    Attributes:
        id: The UUID of the budget.
        user_id: The UUID of the user.
        category: The category of the budget.
        frequency: The frequency of the budget.
        amount: The amount of the budget.

    Relationships:
        user: The user to whom the budget belongs.
    """
    __tablename__ = "budget"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey(USER_ACCOUNT_ID),
                                   nullable=False)
    category: TransactionCategory = db.Column(Enum(TransactionCategory),
                                              nullable=False,
                                              unique=True)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=False)
    amount: int = db.Column(db.Integer,
                            nullable=False)

    user = db.relationship("User", back_populates="budgets")

    def to_dict(self) -> dict:
        """Convert the instance to a dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "category": self.category.name,
            "frequency": self.frequency.name,
            "amount": self.amount
        }
