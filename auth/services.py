import datetime
import os
import uuid
from typing import Final

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import (InvalidHashError, VerificationError,
                               VerifyMismatchError)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.extensions import db
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


def authenticate(email: str, password: str) -> uuid.UUID | None:
    """Authenticate a user.

    Authenticates a user by comparing the provided email and password with the stored email and password.

    Args:
        email, str: the email address of the user
        password, str: the unhashed password provided in the login attempt

    Returns:
        User: the User object if the email and password are correct
        None: if the email and password are incorrect
    """
    try:
        user = db.session.execute(
            select(User.id, User.password).where(User.email == email)
        ).first()
        if user and PH.verify(user.password, password):
            user_id = user[0]
            return user_id
    except VerifyMismatchError:
        print("Incorrect email or password provided.")
        return None
    except VerificationError as e:
        print(f"Verification failed: {e}")
        return None
    except InvalidHashError:
        print("The stored hash is invalid or corrupted.")
        return None


def generate_token(user_id: uuid.UUID) -> str:
    """Generate a JWT token.

    Args:
        user_id, uuid.UUID: the UUID of the user

    Raises:
        ValueError: if the JWT_SECRET_KEY environment variable is not set

    Returns:
        str: the JWT token
    """
    if not os.environ["JWT_SECRET_KEY"]:
        print("JWT_SECRET_KEY environment variable not set.")
        raise ValueError

    payload = {
        'user_id': str(user_id),
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.now()
    }
    token = jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm='HS256')
    return token


def verify_token(token: str) -> str | bool:
    """Verify a JWT token.

    Args:
        token, str: the JWT token to be verified

    Returns:
        str: the UUID of the user if the token is valid
        bool: False if the token is invalid
    """
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=['HS256'])
        user_id = payload['user_id']
        return user_id
    except jwt.ExpiredSignatureError:
        print("Token has expired!")
        return False
    except jwt.InvalidTokenError:
        print("Invalid token!")
        return False
