import datetime
import os
import uuid
from functools import wraps
from typing import Callable, Final

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from backend.extensions import logger
from backend.queries.auth_queries import get_user_by
from flask import g, jsonify, request
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
        "user_id": str(user_id),
        "exp": expiry_time,
        "iat": datetime.datetime.now(),
    }
    token = jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")

    return token, int(expiry_time.timestamp())


def verify_token(token: str) -> str:
    if not token:
        raise ValueError("JWT is missing")

    try:
        decoded_token = jwt.decode(
            token, os.environ["JWT_SECRET_KEY"], algorithms=["HS256"]
        )
        return decoded_token["user_id"]
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError()
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError()


def get_token_from_header(header: str) -> str | None:
    if not header or not header.startswith("Bearer "):
        return None
    return header[7:]


def login_required(f: Callable) -> Callable:
    """Decorator to protect routes by requiring a valid JWT token stored in a cookie.

    If the token is valid, it sets Flask session `g.user_id` with the user's UUID.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("jwt")
        if not token:
            logger.info("No token to authenticate.")
            return jsonify({"auth": False, "message": "No token present."}), 401

        try:
            user_id = verify_token(token)
            if not user_id:
                logger.warning(
                    "Bad Authentication. No `user_id` returned by verify_token()."
                )
                return jsonify({"auth": False, "message": "Bad authentication."}), 401
        except jwt.ExpiredSignatureError as e:
            logger.info(e)
            return jsonify({"auth": False, "message": "Session expired."}), 401
        except jwt.InvalidSignatureError as e:
            logger.warning(e)
            return jsonify({"auth": False, "message": "Invalid token."}), 401

        g.user_id = user_id
        return f(*args, **kwargs)

    return decorated_function
