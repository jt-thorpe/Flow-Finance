import datetime
import os
import uuid
from typing import Final

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import (InvalidHashError, VerificationError,
                               VerifyMismatchError)
from backend.queries.auth_queries import get_user_by
from flask import g
from sqlalchemy.exc import SQLAlchemyError

PH: Final[PasswordHasher] = PasswordHasher()


def hash_password(password: str) -> str:
    """A "wrapper" function for argon2.PasswordHasher.hash().

    Currently don't know why I'm bothering to have this in it's own function. I think the idea was
    to have it in it's own wrapper so that additional logic can be used in the hash process.
    This isn't currently the case however.

    Args:
        password, str: the password to be hashed

    Returns:
        str, the hashed password
    """
    return PH.hash(password)


def authenticate(email: str, password: str) -> bool:
    """Authenticate a user by email and password, setting `g.user_id` if successful.

    Args:
        email (str): The user's email.
        password (str): The unhashed password provided in the login attempt.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    try:
        user = get_user_by(email=email)

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

    expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=60)

    payload = {
        'user_id': str(user_id),
        'exp': expiry_time,
        'iat': datetime.datetime.now()
    }
    token = jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm='HS256')

    return token, int(expiry_time.timestamp())


def verify_token(token: str) -> str:
    if not token:
        raise ValueError("JWT is missing")

    try:
        decoded_token = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=["HS256"])
        return decoded_token["user_id"]
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("JWT signature expired")
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError("JWT is invalid")
