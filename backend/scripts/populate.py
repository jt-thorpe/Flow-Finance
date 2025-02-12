import os
from datetime import timedelta

from auth.services import hash_password
from budgets.models import Budget
from core.app import app
from core.extensions import db
from sqlalchemy import select, text
from transactions.enums import Frequency, TransactionCategory
from transactions.models import Transaction, TransactionType
from users.models import User

"""A script to populate the database with test data."""

# Flask app configuration
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']  # for session
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLOW_DB_URI']  # for PSQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)


def reset_database():
    """Drops all tables in the database and recreates them."""

    def _drop_all():
        """SQLAlchemy doesn't provide a CASCADE drop_all method, so we have to do it manually."""
        for table in db.metadata.sorted_tables:
            db.session.execute(text(f"DROP TABLE IF EXISTS {table.name} CASCADE"))
            db.session.commit()

    with app.app_context():
        _drop_all()
        db.create_all()
    print("Database reset.")


def add_test_user():
    """Adds a test user to the database."""
    print("Adding test user...")
    h_password = hash_password("password")
    test_user = User(email="example@mail.com", password=h_password, alias="Captain Test")
    db.session.add(test_user)
    db.session.commit()
    print("Test user added.")


def get_test_user_id():
    """Gets the user_id of the test user."""
    print("Getting test user_id...")
    return db.session.execute(
        select(User.id).where(User.email == "example@mail.com")
    ).first()


def add_test_income(test_user_id):
    print("Adding test income data...")
    test_income_1 = Transaction(user_id=test_user_id,
                                type=TransactionType.INCOME,
                                category=TransactionCategory.SALARY,
                                date="2021-01-01",
                                frequency=Frequency.MONTHLY,
                                amount=2000,
                                description="An example of some income")
    test_income_2 = Transaction(user_id=test_user_id,
                                type=TransactionType.INCOME,
                                category=TransactionCategory.INTEREST,
                                date="2021-01-01",
                                frequency=Frequency.ANNUALLY,
                                amount=100,
                                description="An example of some interest")
    db.session.add(test_income_1)
    db.session.add(test_income_2)
    db.session.commit()
    print("Test income data added.")


def add_test_expense(test_user_id):
    print("Adding test expense data...")
    test_expense_1 = Transaction(user_id=test_user_id,
                                 type=TransactionType.EXPENSE,
                                 amount=100,
                                 description="Test transaction 1",
                                 date="2021-01-01",
                                 category=TransactionCategory.RENT)
    test_expense_2 = Transaction(user_id=test_user_id,
                                 type=TransactionType.EXPENSE,
                                 amount=50,
                                 description="Test transaction 2",
                                 date="2021-01-02",
                                 category=TransactionCategory.MORTGAGE)
    test_expense_3 = Transaction(user_id=test_user_id,
                                 type=TransactionType.EXPENSE,
                                 amount=75.25,
                                 description="Test transaction 3",
                                 date="2021-01-03",
                                 category=TransactionCategory.UTILITIES)
    test_expense_4 = Transaction(user_id=test_user_id,
                                 type=TransactionType.EXPENSE,
                                 amount=33,
                                 description="Test transaction 4",
                                 date="2021-01-04",
                                 category=TransactionCategory.UTILITIES)
    db.session.add(test_expense_1)
    db.session.add(test_expense_2)
    db.session.add(test_expense_3)
    db.session.add(test_expense_4)
    db.session.commit()
    print("Test expense data added.")


def add_test_budgets(test_user_id):
    print("Adding test budget data...")
    test_budget_1 = Budget(user_id=test_user_id,
                           category=TransactionCategory.RENT,
                           frequency=Frequency.MONTHLY,
                           amount=500.50)
    test_budget_2 = Budget(user_id=test_user_id,
                           category=TransactionCategory.MORTGAGE,
                           frequency=Frequency.MONTHLY,
                           amount=300.33)
    test_budget_3 = Budget(user_id=test_user_id,
                           category=TransactionCategory.UTILITIES,
                           frequency=Frequency.FOUR_WEEKLY,
                           amount=200)
    db.session.add(test_budget_1)
    db.session.add(test_budget_2)
    db.session.add(test_budget_3)
    db.session.commit()
    print("Test budget data added.")


def main():
    with app.app_context():
        print("===== Resetting database ====")
        reset_database()

        print("===== Adding test user(s) to the database =====")
        add_test_user()
        test_user_id = get_test_user_id()[0]
        print(f"Test user_id: {test_user_id}")

        print("===== Adding test income to the database =====")
        add_test_income(test_user_id)

        print("===== Adding test expenses to the database =====")
        add_test_expense(test_user_id)

        print("===== Adding test budgets to the database =====")
        add_test_budgets(test_user_id)

        print("===== Database population complete =====")
        print("Closing database connection...")
        db.session.close()
        print("Database connection closed.")

        print("===== Exiting populate.py =====")


if __name__ == "__main__":
    main()
