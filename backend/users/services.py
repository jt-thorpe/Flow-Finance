from typing import Dict

from core.extensions import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload

from .models import User


def is_taken(email: str) -> bool:
    """True if email is in use by another user."""
    result = db.session.query(User.email).filter(User.email == email).scalar()
    print(f"{__name__} - result = {result}")

    return result is not None


def add_user_account_to_db(email: str, hashed_password: str, alias: str) -> None:
    """Add a user account to the database.

    Args:
        email, str: the email address of the user
        hashed_password, str: the hashed password of the user

    Raises:
        IntegrityError: if the email is already in use
        SQLAlchemyError: if an unexpected error occurs
    """
    try:
        user = User(email=email, password=hashed_password, alias=alias)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        print(f"Integrity error: {str(e)}")
        raise
    except SQLAlchemyError as e:
        print(f"SQLAlchemy error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def get_user_with_associations(user_id: str) -> User:
    """Get a user object with associated data.

    For the authenticated user_id we query all information to create an instance of a User object with associated data from related tables.
    In this case, that is the incomes, expenses, and budgets for said User.id.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        User: the User object with associated data such as incomes, expenses, and budgets.
    """
    return User.query.options(
        joinedload(User.incomes),
        joinedload(User.expenses),
        joinedload(User.budgets)
    ).get(user_id)


def serialise_user_associations(user: User) -> Dict:
    """Serialise the associations of the user object.

    Args:
        user, User: the User object with associated data such as incomes, expenses, and budgets.

    Returns:
        dict: a dictionary containing the user ID, incomes, expenses, and budgets.
    """
    return {
        "id": str(user.id),
        "alias": user.alias,
        "incomes": [income.to_dict() for income in user.incomes],
        "expenses": [expense.to_dict() for expense in user.expenses],
        "budgets": [budget.to_dict() for budget in user.budgets]
    }
