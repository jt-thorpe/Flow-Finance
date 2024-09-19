from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)

from flow.backend.postgresql.connect import get_db_connection

app = Flask(__name__, template_folder='/app/flow/frontend/templates/')  # prepend /app/ for Docker

app.secret_key = 'your_secret_key'  # Needed for session management

# Dummy user data for example purposes
users = {'user@example.com': 'password123'}


@app.route('/')
def home():
    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute('SELECT version();')

    db_version = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('index.html', title="My Budget App", db_version=db_version)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        # Check if user exists and password is correct
        if email in users and users[email] == password:
            session['user'] = email
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

    # GET request: serve login page
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Only allow access to dashboard if the user is logged in
    if 'user' in session:
        return f'Hello, {session["user"]}! Welcome to the dashboard.'
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from session
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
