from typing import Literal

from backend.extensions import db
from backend.models.budget_models import Budget
from backend.models.transaction_models import Transaction
from sqlalchemy.orm.attributes import InstrumentedAttribute


def get_n_user_transactions_ordered(
    user_id: str,
    ordered_by: InstrumentedAttribute = Transaction.date,
    order: Literal["ASC", "DESC"] = "DESC",
    N: int = 10,
) -> list:
    """Get a limited number of transactions for a user, ordered by a specified column and direction.

    Args:
        user_id (str): The UUID of the user.
        ordered_by (InstrumentedAttribute): The column to order by (default is Transaction.date).
        N (int): The number of transactions to return.
        order (Literal["ASC", "DESC"]): The order direction; "ASC" for ascending or "DESC" (default) for descending.

    Returns:
        list: A list of Transaction objects ordered by the specified criteria.
    """
    if order.upper() == "ASC":
        ordering = ordered_by.asc()
    elif order.upper() == "DESC":
        ordering = ordered_by.desc()
    else:
        raise ValueError("order must be either 'ASC' or 'DESC'")

    return (
        db.session.query(Transaction)
        .filter_by(user_id=user_id)
        .order_by(ordering)
        .limit(N)
        .all()
    )


def get_category_totals_by(user_id: str) -> dict[str, float]:
    """Get the total amount spent for each category for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        dict[str, float]: a dictionary of {category: total_spent}.
    """
    # TODO: a VIEW is potentially better here, no built-in SQLAlchemy support however

    category_totals = (
        db.session.query(
            Transaction.category, db.func.sum(Transaction.amount).cast(db.Float)
        )  # Not entirely sure why need to cast back to float
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
    budgets = db.session.query(Budget).where(Budget.user_id == user_id).all()

    return budgets
