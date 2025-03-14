from typing import Dict

from backend.services.transactions_services import (
    get_budgets_by, get_category_totals_by, get_n_user_transactions_ordered)
from flask import g


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
            'frequency': budget.frequency.value,
            'amount': budget.amount,
            'spent': budgets_category_totals.get(budget.category.value, 0),
            'remaining': budget.amount - budgets_category_totals.get(budget.category.value, 0)
        }
        for budget in budgets
    ]


def compute_dashboard(user_data: Dict) -> Dict:
    """Compute and return the required data for displaying on the /dashboard page in a JSON serialisable format."""
    user_id = g.user_id

    latest_transactions = [tx.to_dict()for tx in get_n_user_transactions_ordered(user_id=user_id, N=10)]
    incomes_total = sum(income["amount"] for income in user_data["transactions"] if income["type"] == "income")
    expenses_total = sum(expense["amount"] for expense in user_data["transactions"] if expense["type"] == "expense")
    budget_summary = create_budget_summary(user_data["meta"]["id"])

    return {
        "user_alias": user_data["meta"]["alias"],
        "user_latest_transactions": latest_transactions,
        "user_incomes_total": incomes_total,
        "user_expenses_total": expenses_total,
        "user_budget_summary": budget_summary,
    }
