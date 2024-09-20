from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask.typing import ResponseClass

from flow.backend.authentication.auth import authenticate
from flow.backend.postgresql.database import (Base, engine, get_db_connection,
                                              get_session)
from flow.backend.postgresql.models import User

app = Flask(__name__,
            template_folder='/app/flow/frontend/templates/',
            static_folder='/app/flow/frontend/static/')  # prepend /app/ for Docker

Base.metadata.create_all(engine)


@app.route('/home')
def home():
    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute('SELECT version();')

    db_version = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('index.html', title="My Budget App", db_version=db_version)


@app.route('/login', methods=['GET'])
def login_serve() -> str:
    """Serve `login.html` page."""
    # TODO: Implement some kind of check for a token etc so don't always have to login if token valid
    # GET request: serve login page
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_authenticate() -> ResponseClass:
    data = request.json
    user = authenticate(data['username'], data['password'])

    if user:
        return redirect(url_for('home'))
    return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
