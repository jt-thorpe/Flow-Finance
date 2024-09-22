from flask import Flask, jsonify, render_template, request, url_for
from sqlalchemy.exc import IntegrityError

from flow.backend.authentication.auth import (authenticate,
                                              register_user_account)
from flow.backend.postgresql.database import engine, get_db_connection
from flow.backend.postgresql.models import Base

app = Flask(__name__,
            template_folder='/app/flow/frontend/templates/',
            static_folder='/app/flow/frontend/static/')  # prepend /app/ for Docker


Base.metadata.create_all(engine)


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
    user = authenticate(data['email'], data['password'])

    if user:
        return jsonify({'success': True, 'redirect': url_for('dashboard_serve')}), 200
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/dashboard', methods=['GET'])
def dashboard_serve() -> str:
    """Serve `dashboard.html` page."""
    return render_template('dashboard.html')


@app.route('/home')
def home():
    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute('SELECT version();')

    db_version = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('index.html', title="My Budget App", db_version=db_version)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
