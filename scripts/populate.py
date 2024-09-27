from sqlalchemy import select

from app import app
from extensions import db
from flow.backend.authentication.auth import _hash_password
from flow.backend.postgresql.models import CategoryName, Transaction, User

"""A script to populate the database with dummy data."""


def main():
    with app.app_context():
        # Add some dummy data to the database
        h_password = _hash_password("password")
        test_user = User(email="example@mail.com", password=h_password)
        db.session.add(test_user)
        db.session.commit()

        test_user_id = db.session.execute(
            select(User.id).where(User.email == "example@mail.com")
        ).first()
        print(f"TEST_USER_ID_HERE =============== {test_user_id}")

        test_transaction_1 = Transaction(user_id=test_user_id[0], amount=100.00,
                                         description="Test transaction 1", date="2021-01-01", category=CategoryName.RENT)
        test_transaction_2 = Transaction(user_id=test_user_id[0], amount=50.00,
                                         description="Test transaction 2", date="2021-01-02", category=CategoryName.MORTGAGE)
        test_transaction_3 = Transaction(user_id=test_user_id[0], amount=75.00,
                                         description="Test transaction 3", date="2021-01-03", category=CategoryName.UTILITIES)
        db.session.add(test_transaction_1)
        db.session.add(test_transaction_2)
        db.session.add(test_transaction_3)
        db.session.commit()
        db.session.close()


if __name__ == "__main__":
    main()
