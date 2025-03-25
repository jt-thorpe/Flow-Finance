from backend.extensions import db
from backend.models.budget_models import Budget


def get_budgets_by(user_id: str) -> list[Budget]:
    """Get all budgets for a user.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        list[Budget]: a list of Budget objects.
    """
    return db.session.query(Budget).where(Budget.user_id == user_id).all()
