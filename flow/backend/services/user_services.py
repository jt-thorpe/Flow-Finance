# services/user_service.py
from typing import Dict

from flask import session
from sqlalchemy.orm import joinedload

from flow.backend.postgresql.models import User


def get_user_with_associations(user_id: str):
    """Get a user object with associated data.

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
        "user_id": session['user_id'],
        "user_incomes": [income.to_dict() for income in user.incomes],
        "user_expenses": [expense.to_dict() for expense in user.expenses],
        "user_budgets": [budget.to_dict() for budget in user.budgets]
    }
