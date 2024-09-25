import uuid
from typing import Optional

from sqlalchemy import Date, Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID

from extensions import db


class User(db.Model):
    """A 'User' class mapped via ORM to the 'user_account' table."""

    __tablename__ = "user_account"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text("gen_random_uuid()"))
    email: str = db.Column(String(100), unique=True, nullable=False)
    password: str = db.Column(String(100), nullable=False)


class Transaction(db.Model):  # Inherit from db.Model
    """A 'Transaction' class mapped via ORM to the 'transaction' table."""

    __tablename__ = "transaction"

    id: uuid.UUID = db.Column(UUID(as_uuid=True),
                              primary_key=True,
                              unique=True,
                              server_default=text("gen_random_uuid()"))
    user_id: uuid.UUID = db.Column(ForeignKey("user_account.id"), nullable=False)
    amount: float = db.Column(Float, nullable=False)
    description: Optional[str] = db.Column(String(100), nullable=True)
    date: Date = db.Column(Date, nullable=False)
    category: Optional[str] = db.Column(String(100), nullable=True)
