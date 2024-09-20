from typing import Final

from argon2 import PasswordHasher
from sqlalchemy import select

from flow.backend.postgresql.database import get_session
from flow.backend.postgresql.models import User

PH: Final[PasswordHasher] = PasswordHasher()


def authenticate(email: str, password: str):
    hashed_email, hashed_password = PH.hash(email), PH.hash(password)
    session = get_session()
    try:
        user = session.execute(select(User)).where(User.email == hashed_email)
        if user and PH.verify(user.password, hashed_password):
            return user  # Return the User object if successful
        return None  # Authentication failed
    finally:
        session.close()
