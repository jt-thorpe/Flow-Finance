
from typing import Final

from argon2 import PasswordHasher
from sqlalchemy import select

from backend.extensions import db
from backend.models.user_models import User

PH: Final[PasswordHasher] = PasswordHasher()


def get_user_by(email: str):
    # TODO: Document and err handle
    return db.session.execute(
        select(User.id, User.password).where(User.email == email)
    ).first()
