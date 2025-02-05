from datetime import datetime
from typing import Dict

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


def compute_dashboard(user_data: Dict) -> Dict:
    """Compute and return the required data for displaying on the /dashboard page in a JSON serialisable format."""
    combined_transactions = [
        {**item, "type": "income"} for item in user_data['incomes']
    ] + [
        {**item, "type": "expense"} for item in user_data['expenses']
    ]
    combined_transactions.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    incomes_total = sum(income["amount"] for income in user_data["incomes"])
    expenses_total = sum(expense["amount"] for expense in user_data["expenses"])
    budget_summary = create_budget_summary(user_data["meta"]["id"])

    return {
        "user_alias": user_data["meta"]["alias"],
        "user_latest_transactions": combined_transactions[:10],  # Latest 10
        "user_incomes_total": incomes_total,
        "user_expenses_total": expenses_total,
        "user_budget_summary": budget_summary,
    }
