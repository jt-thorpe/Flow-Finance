import enum
import uuid
from typing import Final, Optional

from sqlalchemy import Date, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from extensions import db

GEN_RANDOM_UUID: Final[str] = "gen_random_uuid()"


class User(db.Model):
    """A 'User' class mapped via ORM to the 'user_account' table."""
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


class CategoryName(enum.Enum):
    RENT = "rent"
    MORTGAGE = "mortgage"
    UTILITIES = "utilities"
    SUBSCRIPTION = "subscription"
    LEISURE = "leisure"
    GROCERIES = "groceries"
    DINING = "dining"
    ALCOHOL = "alcohol"
    HEALTH = "health"
    SPORT = "sport"
    GIGS = "gigs"
    EVENT = "event"


class Transaction(db.Model):
    """Models a user's financial transactions."""
    __tablename__ = "transaction"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey("user_account.id"),
                                   nullable=False)
    date: Date = db.Column(db.Date,
                           nullable=False)
    amount: float = db.Column(db.Float,
                              nullable=False)
    category: CategoryName = db.Column(Enum(CategoryName),
                                       nullable=False)
    description: Optional[str] = db.Column(String(100),
                                           nullable=True)


class Budget(db.Model):
    """Models a user's budget for a given category."""

    __tablename__ = "budget"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text(GEN_RANDOM_UUID))
    user_id: uuid.UUID = db.Column(ForeignKey("user_account.id"),
                                   nullable=False)
    category: CategoryName = db.Column(Enum(CategoryName),
                                       nullable=False,
                                       unique=True)
    amount: float = db.Column(db.Float,
                              nullable=False)
