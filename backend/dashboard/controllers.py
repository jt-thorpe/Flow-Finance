"""In here we will have the controllers for the transactions.

So things like creating a new income, expense, budget, etc. will be done here.

E.g. we will need routes for creating/modifying budgets, and a page for viewing transactions.
"""
from datetime import datetime

from auth.controllers import login_required
from cache.services import cache_user_with_associations, get_user_cache
from dashboard.services import create_budget_summary
from flask import Blueprint, jsonify, request
from users.services import get_user_with_associations

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_blueprint.route('/load', methods=['GET'])
@login_required
def load_dashboard():
    # Check the cache first
    user_data = get_user_cache(request.user_id)

    if not user_data:
        # If not cached, fetch from the database
        user_data = get_user_with_associations(user_id=request.user_id)

        if not user_data:
            return jsonify({'success': False, 'message': f"{__name__} - Error fetching user data from db."}), 404

        # Store in Redis for future requests
        cache_user_with_associations(user_data)

        # # This serialisation needs to be done earlier, somewhere else, otherwise we're going to be serialising it all over the place...
        # user_data = serialise_user_associations(user_data)

    combined_transactions = [
        {**item, "type": "income"} for item in user_data['incomes']
    ] + [
        {**item, "type": "expense"} for item in user_data['expenses']
    ]
    combined_transactions.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)
    incomes_total = sum(income["amount"] for income in user_data["incomes"])
    expenses_total = sum(expense["amount"] for expense in user_data["expenses"])
    budget_summary = create_budget_summary(request.user_id)

    print(combined_transactions)
    print(incomes_total)
    print(expenses_total)
    print(budget_summary)

    return jsonify({
        "user_alias": user_data["meta"]["alias"],
        "user_latest_transactions": combined_transactions[:10],  # Latest 10
        "user_incomes_total": incomes_total,
        "user_expenses_total": expenses_total,
        "user_budget_summary": budget_summary,
    }), 200
