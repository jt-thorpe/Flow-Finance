from sqlalchemy import select, text

from flow.app import app
from flow.backend.auth.services import _hash_password
from flow.backend.transactions.enums import Frequency, TransactionCategory
from flow.backend.transactions.models import Budget, Expense, Income
from flow.backend.users.models import User
from flow.extensions import db

"""A script to populate the database with test data."""


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
    h_password = _hash_password("password")
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
    test_income_1 = Income(user_id=test_user_id,
                           category=TransactionCategory.SALARY,
                           date="2021-01-01",
                           frequency=Frequency.MONTHLY,
                           amount=200000,
                           description="An example of some income")
    test_income_2 = Income(user_id=test_user_id,
                           category=TransactionCategory.INTEREST,
                           date="2021-01-01",
                           frequency=Frequency.ANNUALLY,
                           amount=10000,
                           description="An example of some interest")
    db.session.add(test_income_1)
    db.session.add(test_income_2)
    db.session.commit()
    print("Test income data added.")


def add_test_expense(test_user_id):
    print("Adding test expense data...")
    test_expense_1 = Expense(user_id=test_user_id,
                             amount=10000,
                             description="Test transaction 1",
                             date="2021-01-01",
                             category=TransactionCategory.RENT)
    test_expense_2 = Expense(user_id=test_user_id,
                             amount=5000,
                             description="Test transaction 2",
                             date="2021-01-02",
                             category=TransactionCategory.MORTGAGE)
    test_expense_3 = Expense(user_id=test_user_id,
                             amount=7500,
                             description="Test transaction 3",
                             date="2021-01-03",
                             category=TransactionCategory.UTILITIES)
    test_expense_4 = Expense(user_id=test_user_id,
                             amount=3300,
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
                           amount=50000)
    test_budget_2 = Budget(user_id=test_user_id,
                           category=TransactionCategory.MORTGAGE,
                           frequency=Frequency.MONTHLY,
                           amount=30000)
    test_budget_3 = Budget(user_id=test_user_id,
                           category=TransactionCategory.UTILITIES,
                           frequency=Frequency.FOUR_WEEKLY,
                           amount=20000)
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
