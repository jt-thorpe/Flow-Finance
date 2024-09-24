from flask import (Flask, jsonify, make_response, render_template, request,
                   url_for)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from flow.backend.authentication.auth import (_hash_password, authenticate,
                                              generate_token, login_required,
                                              register_user_account)
from flow.backend.postgresql.database import (engine, get_db_connection,
                                              get_session,
                                              get_user_transactions)
from flow.backend.postgresql.models import Base, Transaction, User

app = Flask(__name__,
            template_folder='/app/flow/frontend/templates/',
            static_folder='/app/flow/frontend/static/')  # prepend /app/ for Docker


Base.metadata.create_all(engine)


# ###
# # Add some dummy data to the database
# session = get_session()

# # h_password = _hash_password("password")
# # test_user = User(email="example@mail.com", password=h_password)
# # session.add(test_user)
# # session.commit()

# test_user_id = session.execute(
#     select(User.id).where(User.email == "example@mail.com")
# ).first()
# print(f"TEST_USER_ID_HERE =============== {test_user_id}")

# test_transaction_1 = Transaction(user_id=test_user_id[0], amount=100.00,
#                                  description="Test transaction 1", date="2021-01-01", category="food")
# test_transaction_2 = Transaction(user_id=test_user_id[0], amount=50.00,
#                                  description="Test transaction 2", date="2021-01-02", category="drink")
# test_transaction_3 = Transaction(user_id=test_user_id[0], amount=75.00,
#                                  description="Test transaction 3", date="2021-01-03", category="utility")
# session.add(test_transaction_1)
# session.add(test_transaction_2)
# session.add(test_transaction_3)
# session.commit()
# session.close()
# ###


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
    return render_template('dashboard.html',
                           transactions=get_user_transactions(user_id=user_id))


@app.route('/home')
@login_required
def home():
    # TODO: Eventually will be the homepage of the website.
    conn = get_db_connection()

    cur = conn.cursor()
    cur.execute('SELECT version();')

    db_version = cur.fetchone()

    cur.close()
    conn.close()

    return render_template('index.html', title="My Budget App", db_version=db_version)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
