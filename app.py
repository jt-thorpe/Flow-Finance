import os

from flask import (Flask, jsonify, make_response, render_template, request,
                   url_for)
from sqlalchemy.exc import IntegrityError

from extensions import db
from flow.backend.authentication.auth import (authenticate, generate_token,
                                              login_required,
                                              register_user_account)
from flow.backend.postgresql.queries import get_n_transactions

app = Flask(__name__,
            template_folder='/app/flow/frontend/templates/',
            static_folder='/app/flow/frontend/static/')  # prepend /app/ for Docker
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLOW_DB_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    # TODO: Implement some kind of check for a token etc so don't always have to login if token valid
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_authenticate():
    data = request.json
    user_id = authenticate(data['email'], data['password'])
    print(f"USER =============== {user_id}")

    if user_id:
        token = generate_token(user_id=user_id)
        print(f"TOKEN =============== {token}")
        response = make_response(jsonify({'success': True, 'redirect': url_for('dashboard_serve')}), 200)
        response.set_cookie('jwt_token', token, httponly=True, secure=True, samesite='Strict')
        return response
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard_serve() -> str:
    """Serve `dashboard.html` page."""
    user_id = request.user_id
    latest_transactions = get_n_transactions(user_id=user_id, N=10)
    return render_template('dashboard.html',
                           transactions=latest_transactions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
