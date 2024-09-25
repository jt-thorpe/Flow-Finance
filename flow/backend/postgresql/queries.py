from extensions import db
from flow.backend.postgresql.models import Transaction, User


def get_n_transactions(user_id: str, N: int = 10) -> list[Transaction]:  # Hint might be wrong
    """Get N-many recent transactions for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.
        N, int: the number of transactions to return.

    Returns:
        list[Transaction]: a list of Transaction objects.
    """
    transactions = (
        db.session.query(Transaction)
        .join(User)
        .filter(User.id == user_id)
        .order_by(Transaction.date.desc())
        .limit(N)
        .all()
    )

    return transactions
