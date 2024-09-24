import uuid
from typing import List

from sqlalchemy import Date, Float, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column)


class Base(DeclarativeBase):
    pass


class User(MappedAsDataclass, Base):
    """A 'User' dataclass which is mapped via ORM to a 'user' table.

    A value for User.id should not be passed when creating a User. The generation of
    User.id is handled explicitly by the database.
    """

    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                          init=False,
                                          primary_key=True,
                                          unique=True,
                                          server_default=text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))

    # Saw this in an SQLAlchemy example, but not sure if I want this behavior
    # transactions: Mapped[List["Transaction"]] = relationship(back_populates="user")  # user field in Transaction


class Transaction(MappedAsDataclass, Base):
    """A 'Transaction' dataclass which is mapped via ORM to a 'transaction' table.

    A value for Transaction.id should not be passed when creating a Transaction. The generation of
    Transaction.id is handled explicitly by the database.
    """

    __tablename__ = "transaction"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                          init=False,
                                          primary_key=True,
                                          unique=True,
                                          server_default=text("gen_random_uuid()"))
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)  # Check Date type is appropriate
    category: Mapped[str] = mapped_column(String(100), nullable=True)

    # Saw this in an SQLAlchemy example, but not sure if I want this behavior
    # user: Mapped["User"] = relationship(back_populates="transactions")  # transactions field in User
