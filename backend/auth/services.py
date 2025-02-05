import datetime
import os
import uuid
from typing import Final

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import (InvalidHashError, VerificationError,
                               VerifyMismatchError)
from core.extensions import db
from flask import g
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from users.models import User

PH: Final[PasswordHasher] = PasswordHasher()


def _hash_password(password: str) -> str:
    """A "wrapper" function for argon2.PasswordHasher.hash().

    Currently don't know why I'm bothering to have this in it's own function. I think the idea was
    to have it in it's own wrapper so that additional logic can be used in the hash process.
    This isn't currently the case however.

    #TODO Remove probably?

    Args:
        password, str: the password to be hashed

    Returns:
        str, the hashed password
    """
    return PH.hash(password)


def _add_user_account_to_db(email: str, hashed_password: str) -> None:
    """Add a user account to the database.

    Args:
        email, str: the email address of the user
        hashed_password, str: the hashed password of the user

    Raises:
        IntegrityError: if the email is already in use
        SQLAlchemyError: if an unexpected error occurs
    """
    try:
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        print(f"Integrity error: {str(e)}")
        raise
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def register_user_account(email: str, password: str) -> None:
    """Register a user account.

    Represents the user registration process. The password is hashed and stored in the database.

    Args:
        email, str: the email address of the user
        password, str: the password of the user
    """
    _add_user_account_to_db(email=email,
                            hashed_password=_hash_password(password=password))


def authenticate(email: str, password: str) -> bool:
    """Authenticate a user by email and password, setting `g.user_id` if successful.

    Args:
        email (str): The user's email.
        password (str): The unhashed password provided in the login attempt.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    try:
        user = db.session.execute(
            select(User.id, User.password).where(User.email == email)
        ).first()

        if user and PH.verify(user.password, password):
            g.user_id = user[0]
            return True

    except VerifyMismatchError:
        print("Incorrect email or password provided.")
    except VerificationError as e:
        print(f"Verification failed: {e}")
    except InvalidHashError:
        print("The stored hash is invalid or corrupted.")
    except SQLAlchemyError as e:
        print(f"Database error during authentication: {e}")

    return False


def generate_token(user_id: uuid.UUID) -> tuple[str, int]:
    """Generate a JWT token and return expiry time."""
    if not os.environ.get("JWT_SECRET_KEY"):
        raise ValueError("JWT_SECRET_KEY is missing")

    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=1)

    payload = {
        'user_id': str(user_id),
        'exp': expiry_time,
        'iat': datetime.datetime.now()
    }
    token = jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm='HS256')

    return token, int(expiry_time.timestamp())


def verify_token(token: str) -> str | None:
    """Verifies JWT token and returns the user ID if valid."""
    try:
        decoded_token = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=["HS256"])
        return decoded_token.get("user_id")
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"
    except Exception as e:
        print(f"Unexpected JWT error: {e}")
        return None
