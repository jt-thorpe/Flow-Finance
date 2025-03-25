from typing import List, Literal

from backend.extensions import db
from backend.models.transaction_models import Transaction
from sqlalchemy.orm.attributes import InstrumentedAttribute


def get_all_transactions(user_id: str) -> List[Transaction]:
    """Get all transactions for a user_id."""
    return (
        Transaction.query.where(Transaction.user_id == user_id)
        .order_by(Transaction.date.desc())
        .all()
    )


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
    category_totals = (
        db.session.query(
            Transaction.category, db.func.sum(Transaction.amount).cast(db.Float)
        )  # Not entirely sure why need to cast back to float
        .filter(Transaction.user_id == user_id)
        .group_by(Transaction.category)
        .all()
    )

    return {category.value: total for category, total in category_totals}
