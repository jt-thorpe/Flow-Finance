from typing import Dict

from backend.queries.transactions_queries import get_n_user_transactions_ordered
from backend.services.budget_services import create_budget_summary
from flask import g


def compute_dashboard(user_data: Dict) -> Dict:
    """Compute and return the required data for displaying on the /dashboard page in a JSON serialisable format."""
    user_id = g.user_id

    latest_transactions = [
        tx.to_dict() for tx in get_n_user_transactions_ordered(user_id=user_id, N=10)
    ]
    incomes_total = sum(
        income["amount"]
        for income in user_data["transactions"]
        if income["type"] == "income"
    )
    expenses_total = sum(
        expense["amount"]
        for expense in user_data["transactions"]
        if expense["type"] == "expense"
    )
    budget_summary = create_budget_summary(user_data["meta"]["id"])

    return {
        "user_alias": user_data["meta"]["alias"],
        "user_latest_transactions": latest_transactions,
        "user_incomes_total": incomes_total,
        "user_expenses_total": expenses_total,
        "user_budget_summary": budget_summary,
    }
