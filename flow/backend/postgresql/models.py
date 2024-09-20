from sqlalchemy import String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from flow.backend.postgresql.database import Base


class User(MappedAsDataclass, Base):
    """A 'User' dataclass which is mapped via ORM to a 'user' table."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(30))
