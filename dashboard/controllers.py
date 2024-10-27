"""In here we will have the controllers for the transactions.

So things like creating a new income, expense, budget, etc. will be done here.

E.g. we will need routes for creating/modifying budgets, and a page for viewing transactions.
"""
from flask import Blueprint, render_template, session

from auth.controllers import login_required
from cache.services import retrieve_user_data
from dashboard.services import create_budget_summary

dashboard_blueprint = Blueprint('dashboard', __name__)


@dashboard_blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard_serve() -> str:
    """Serve `dashboard.html` page."""
    cached_user_data = retrieve_user_data(session["user_id"])
    return render_template('dashboard.html',
                           user_alias=session["user_alias"],
                           transactions=cached_user_data["user_expenses"],
                           budget_summary=create_budget_summary(session["user_id"]))
