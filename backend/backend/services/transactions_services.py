from backend.extensions import db
from backend.models.budget_models import Budget
from backend.models.transaction_models import Transaction


def get_n_transactions_by(user_id: str, N: int = 10) -> list:
    """Get N-many recent transactions (both income and expense) for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.
        N, int: the number of transactions to return.

    Returns:
        list: a list of Transaction objects (Income or Expense).
    """
    return db.session.query(Transaction).filter_by(user_id=user_id).limit(limit=N).all()


def get_category_totals_by(user_id: str) -> dict[str, float]:
    """Get the total amount spent for each category for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        dict[str, float]: a dictionary of {category: total_spent}.
    """
    # TODO: a VIEW is potentially better here, no built-in SQLAlchemy support however

    category_totals = (
        db.session.query(Transaction.category, db.func.sum(Transaction.amount).cast(
            db.Float))  # Not entirely sure why need to cast back to float
        .filter(Transaction.user_id == user_id)
        .group_by(Transaction.category)
        .all()
    )

    return {category.value: total for category, total in category_totals}


def get_budgets_by(user_id: str) -> list[Budget]:
    """Get all budgets for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        list[Budget]: a list of Budget objects.
    """
    budgets = (
        db.session.query(Budget)
        .where(Budget.user_id == user_id)
        .all()
    )

    return budgets
