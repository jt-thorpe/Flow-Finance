"""In here we will have the controllers for the transactions.

So things like creating a new income, expense, budget, etc. will be done here.

E.g. we will need routes for creating/modifying budgets, and a page for viewing transactions.
"""


from flask import Blueprint, render_template, session

from auth.controllers import login_required
from cache.services import retrieve_user_data_json

transactions_blueprint = Blueprint('transactions', __name__)


@transactions_blueprint.route('/transactions', methods=['GET'])
@login_required
def transactions_server() -> str:
    """Serve `dashboard.html` page."""
    cached_user_data = retrieve_user_data_json(session["user_id"])

    return render_template('transactions.html',
                           user_alias=session["user_alias"],
                           user_incomes=cached_user_data["user_incomes"],
                           user_expenses=cached_user_data["user_expenses"],)
