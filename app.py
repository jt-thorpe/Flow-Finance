import json
import os
from datetime import timedelta

import redis
from flask import (Flask, jsonify, make_response, render_template, request,
                   session, url_for)
from sqlalchemy.exc import IntegrityError

from extensions import db
from flow.backend.authentication.auth import (authenticate, generate_token,
                                              login_required,
                                              register_user_account)
from flow.backend.postgresql.queries import create_budget_summary
from flow.backend.services.user_services import (get_user_with_associations,
                                                 serialise_user_associations)

app = Flask(__name__,
            template_folder='/app/flow/frontend/templates/',
            static_folder='/app/flow/frontend/static/')  # prepend /app/ for Docker

app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']  # for session
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLOW_DB_URI']  # for PSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


# Use the Redis service hostname from docker-compose (it’s called 'redis')
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_cache = redis.Redis(host=redis_host, port=6379, decode_responses=True)
CACHE_EXPIRATION = 60 * 30


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET'])
def register_serve() -> str:
    """Serve `regisster.html` page."""
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        register_user_account(data['email'], data['password'])
        return jsonify({'success': True, 'redirect': url_for('login_serve')}), 200
    except IntegrityError:
        return jsonify({'success': False, 'message': 'Unable to register account. Email already in use.'}), 401


@app.route('/login', methods=['GET'])
def login_serve() -> str:
    """Serve `login.html` page."""
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_authenticate():
    data = request.json
    user_id = authenticate(data['email'], data['password'])
    session['user_id'] = str(user_id)

    if user_id:
        try:
            # Load the user object with associated data
            user = get_user_with_associations(user_id=user_id)
            session['user_alias'] = user.alias

            # Serialise the user object
            serialised_user = serialise_user_associations(user)
            serialised_user_json = json.dumps(serialised_user)

            redis_cache.set(f"user:{session['user_id']}", serialised_user_json, ex=CACHE_EXPIRATION)
        except Exception as e:
            return jsonify({'success': False, 'message': f'Unable to cache user data: {e}'}), 500

        # Generate the token
        token = generate_token(user_id=user.id)

        # Set the token in a cookie
        response = make_response(jsonify({'success': True, 'redirect': url_for('dashboard_serve')}), 200)
        response.set_cookie('jwt_token', token, httponly=True, secure=True, samesite='Strict')
        return response

    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard_serve() -> str:
    """Serve `dashboard.html` page."""
    cached_user_data = json.loads(redis_cache.get(f"user:{session['user_id']}"))
    return render_template('dashboard.html',
                           user_alias=session["user_alias"],
                           transactions=cached_user_data["user_expenses"],
                           budget_summary=create_budget_summary(session["user_id"]))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
