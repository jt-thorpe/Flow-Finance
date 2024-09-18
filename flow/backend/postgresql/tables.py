from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column)


class Base(DeclarativeBase):
    pass


class User(MappedAsDataclass, Base):
    """A 'User' dataclass which is mapped via ORM to a 'User' table."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(String(255))
