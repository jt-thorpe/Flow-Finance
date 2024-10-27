from functools import wraps
from typing import Callable

from flask import (Blueprint, jsonify, make_response, redirect,
                   render_template, request, session, url_for)
from sqlalchemy.exc import IntegrityError

from cache.services import cache_user_with_associations
from users.services import get_user_with_associations

from .services import (authenticate, generate_token, register_user_account,
                       verify_token)

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET'])
def register_serve() -> str:
    """Render the `register.html` page."""
    return render_template('register.html')


@auth_blueprint.route('/register', methods=['POST'])
def register_user():
    """Register a new user account."""
    data = request.json
    try:
        register_user_account(data['email'], data['password'])
        return jsonify({'success': True, 'redirect': url_for('login_serve')}), 200
    except IntegrityError:
        return jsonify({'success': False, 'message': 'Unable to register account. Email already in use.'}), 401


@auth_blueprint.route('/login', methods=['GET'])
def login_serve() -> str:
    """Serve `login.html` page."""
    return render_template('login.html')


@auth_blueprint.route('/login', methods=['POST'])
def login_authenticate():
    """Authenticate a user and generate a JWT token.

    This function authenticates a user by checking the email and password against the database. If the credentials are
    valid, a JWT token is generated and set in a cookie. The user object is then serialised and cached in Redis.

    Returns:
        Response: a JSON response indicating success or failure
    """
    # TODO: separate the authentication logic from the route

    data = request.json
    user_id = authenticate(data['email'], data['password'])
    session['user_id'] = str(user_id)

    if user_id:
        try:
            # Load the user object with associated data
            user = get_user_with_associations(user_id=user_id)
            session['user_alias'] = user.alias
            cache_user_with_associations(user)
        except Exception as e:
            return jsonify({'success': False, 'message': f'Cache service was unable to cache the User object: {e}'}), 500

        # Generate the token
        token = generate_token(user_id=user.id)

        # Set the token in a cookie
        response = make_response(jsonify({'success': True, 'redirect': url_for('dashboard.dashboard_serve')}), 200)
        response.set_cookie('jwt_token', token, httponly=True, secure=True, samesite='Strict')
        return response

    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


def login_required(f: Callable) -> Callable:
    """A decorator to require a user to be logged in to access a route.

    Essentially, this decorator checks if a user is logged in by checking for a JWT token in the cookies. If the token
    is present, it is decoded to extract the user information. If the token is not present or invalid, the user is
    redirected to the login page and the decorated function, i.e. the application route, is not executed.

    Args:
        f: the function to be decorated

    Returns:
        decorated_function: the decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt_token')  # Get JWT from cookies
        if not token:
            return redirect(url_for('auth.login_serve'))

        # Decode the token to extract user information
        user_id = verify_token(token)
        if not user_id:
            return redirect(url_for('auth.login_serve'))

        return f(*args, **kwargs)
    return decorated_function
