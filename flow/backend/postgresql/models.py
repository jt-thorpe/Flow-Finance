import uuid

from sqlalchemy import String, text
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

    # `init=False` ensures we cannot pass `id` when instantiating a User
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                          init=False,
                                          primary_key=True,
                                          unique=True,
                                          server_default=text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(String(100),
                                       unique=True)
    password: Mapped[str] = mapped_column(String(100))
