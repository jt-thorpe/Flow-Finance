from transactions.services import get_budgets_by, get_category_totals_by


def create_budget_summary(user_id: str) -> list[dict]:
    """Create a summary of the user's budgets.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        list[dict]: a list of dictionaries with keys 'category', 'amount', 'spent', 'remaining'.
    """
    budgets = get_budgets_by(user_id)
    budgets_category_totals = get_category_totals_by(user_id)

    return [
        {
            'category': budget.category.value,
            'amount': budget.amount,
            'spent': budgets_category_totals.get(budget.category.value, 0),
            'remaining': budget.amount - budgets_category_totals.get(budget.category.value, 0)
        }
        for budget in budgets
    ]
