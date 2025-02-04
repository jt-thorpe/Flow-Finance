from functools import wraps
from typing import Callable

from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError

from .services import (authenticate, generate_token, register_user_account,
                       verify_token)

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    """Register a new user account."""
    data = request.json
    try:
        register_user_account(data['email'], data['password'])
        return jsonify({'success': True, 'message': 'User registered successfully'}), 201
    except IntegrityError:
        return jsonify({'success': False, 'message': 'Email already in use'}), 400


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = authenticate(data['email'], data['password'])

    if user_id:
        token, expiry = generate_token(user_id=user_id)
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

    If the token is verified, we expose the users UUID at request.user_id.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("jwt")
        if not token:
            return jsonify({'success': False, 'message': 'Missing or invalid token'}), 401

        user_id = verify_token(token)
        if not user_id:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401

        request.user_id = user_id
        return f(*args, **kwargs)

    return decorated_function
