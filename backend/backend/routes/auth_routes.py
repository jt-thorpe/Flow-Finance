from functools import wraps
from typing import Callable

from flask import Blueprint, Response, g, jsonify, make_response, request

from backend.services.auth_services import (authenticate, generate_token,
                                            verify_token)

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
            "token": token,
            "expires_at": expiry
        }), 200)
        response.set_cookie("jwt", token, httponly=True, secure=True, samesite="Lax")
        return response

    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


def login_required(f: Callable) -> Callable:
    """Decorator to protect routes by requiring a valid JWT token stored in a cookie.

    If the token is valid, it sets `g.user_id` with the user's UUID.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("jwt")
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
@login_required
def verify_authenticity() -> tuple[Response, int]:
    """Verifies that the provided token is genuine. Used by the frontend to check auth state."""
    return jsonify({"auth": True}), 200


@auth_blueprint.route("/logout", methods=["POST"])
def logout() -> tuple[Response, int]:
    """Logs the user out."""
    response = make_response(jsonify({"message": "Logged out"}))
    response.set_cookie("jwt", "", expires=0, httponly=True, secure=True, samesite="Lax")
    return response, 200
