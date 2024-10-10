import uuid
from typing import Final, Optional

from sqlalchemy import Date, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from extensions import db
from flow.backend.postgresql.enums import (ExpenseCategory, Frequency,
                                           IncomeCategory)

GEN_RANDOM_UUID: Final[str] = "gen_random_uuid()"


class User(db.Model):
    """A 'User' class mapped via ORM to the 'user_account' table.

    Attributes:
        id: The UUID of the user.
        email: The email address of the user.
        password: The hashed password of the user.
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


class Income(db.Model):
    """Models a user's finacial income.

    Attributes:
        id: The UUID of the income.
        user_id: The UUID of the user.
        category: The category of the income.
        date: The date of the income.
        frequency: The frequency of the income.
        amount: The amount of the income.
        description: A description of the income.
    """
    __tablename__ = "income"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey("user_account.id"),
                                   nullable=False)
    category: IncomeCategory = db.Column(Enum(IncomeCategory),
                                         nullable=False)
    date: Date = db.Column(db.Date,
                           nullable=False)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=True)
    amount: float = db.Column(db.Float,
                              nullable=False)
    description: Optional[str] = db.Column(String(100),
                                           nullable=True)


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
    """
    __tablename__ = "expense"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey("user_account.id"),
                                   nullable=False)
    category: ExpenseCategory = db.Column(Enum(ExpenseCategory),
                                          nullable=False)
    date: Date = db.Column(db.Date,
                           nullable=False)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=True)
    amount: float = db.Column(db.Float,
                              nullable=False)

    description: Optional[str] = db.Column(String(100),
                                           nullable=True)


class Budget(db.Model):
    """Models a user's budget for a given expense category.

    Attributes:
        id: The UUID of the budget.
        user_id: The UUID of the user.
        category: The category of the budget.
        frequency: The frequency of the budget.
        amount: The amount of the budget.
    """

    __tablename__ = "budget"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey("user_account.id"),
                                   nullable=False)
    category: ExpenseCategory = db.Column(Enum(ExpenseCategory),
                                          nullable=False,
                                          unique=True)
    frequency: Frequency = db.Column(Enum(Frequency),
                                     nullable=False)
    amount: float = db.Column(db.Float,
                              nullable=False)
