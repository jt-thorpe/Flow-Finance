from budgets.models import Budget
from core.extensions import db
from sqlalchemy import select
from transactions.models import Expense, Income


def get_n_transactions(user_id: str, N: int = 10) -> list:
    """Get N-many recent transactions (both income and expense) for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.
        N, int: the number of transactions to return.

    Returns:
        list: a list of Transaction objects (Income or Expense).
    """
    stmt = select(Income, Expense).join(Income.user_id).where(
        Income.user_id == user_id).order_by("date desc").limit(N)
    res = db.session.execute(stmt).fetchall()

    return res


def get_category_totals_by(user_id: str) -> dict[str, float]:
    """Get the total amount spent for each category for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        dict[str, float]: a dictionary of {category: total_spent}.
    """
    # TODO: a VIEW is potentially better here, no built-in SQLAlchemy support however

    category_totals = (
        db.session.query(Expense.category, db.func.sum(Expense.amount).cast(
            db.Float))  # Not entirely sure why need to cast back to float
        .filter(Expense.user_id == user_id)
        .group_by(Expense.category)
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
