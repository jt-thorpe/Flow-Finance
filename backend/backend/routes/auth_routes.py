from functools import wraps
from typing import Callable

import jwt
from backend.extensions import logger
from backend.services.auth_services import (authenticate, generate_token,
                                            get_token_from_header,
                                            verify_token)
from flask import Blueprint, Response, g, jsonify, make_response, request

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    email, password = data.get("email"), data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    if authenticate(email, password):
        token, expiry = generate_token(user_id=g.user_id)
        response = make_response(jsonify({
            "message": "Login successful",
            "user_id": g.user_id,  # Ensure frontend receives user data
            "expires_at": expiry
        }), 200)

        response.set_cookie(
            key="jwt",
            value=token,
            expires=expiry,
            path="/",
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response

    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


def login_required(f: Callable) -> Callable:
    """Decorator to protect routes by requiring a valid JWT token stored in a cookie.

    If the token is valid, it sets Flask session `g.user_id` with the user's UUID.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("jwt")
        print(f"Token here = {token}")
        if not token:
            return jsonify({'success': False, 'message': 'Authentication required.'}), 401

        user_id = verify_token(token)

        if user_id == "expired":  # TODO: change this
            return jsonify({'success': False, 'message': 'Session expired. Please log in again.'}), 401
        if user_id == "invalid":  # TODO: change this
            return jsonify({'success': False, 'message': 'Invalid token. Authentication failed.'}), 401
        if not user_id:
            return jsonify({'success': False, 'message': 'Authentication required.'}), 401

        g.user_id = user_id
        return f(*args, **kwargs)

    return decorated_function


@auth_blueprint.route('/verify', methods=['GET'])
def verify_authenticity() -> tuple[Response, int]:
    """Verifies that the provided token is genuine."""
    token = get_token_from_header(
        request.headers.get("Authorization")
    ) if not request.cookies else request.cookies.get("jwt")

    logger.info(f"auth_routes.verify_authenticity : Token is {token}")

    if not token:
        logger.info("auth_routes.verify_authenticity : No token was provided.")
        return jsonify({"auth": False, "message": "No token provided"}), 401

    try:
        user_id = verify_token(token)
    except jwt.ExpiredSignatureError:
        logger.warning("auth_routes.verify_authenticity : Token is EXPIRED.", exc_info=1)
        return jsonify({"auth": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        logger.warning("auth_routes.verify_authenticity : Token is INVALID.", exc_info=1)
        return jsonify({"auth": False, "message": "Invalid token"}), 401

    logger.info("auth_routes.verify_authenticity : Token verification successful.")
    return jsonify({"auth": True, "user_id": user_id}), 200


@auth_blueprint.route("/logout", methods=["POST"])
def logout() -> tuple[Response, int]:
    """Logs the user out."""
    response = make_response(jsonify({"message": "Logged out"}))
    response.set_cookie("jwt",
                        "",
                        expires=0,
                        httponly=True,
                        secure=True,
                        samesite=None,
                        path="/")
    return response, 200
