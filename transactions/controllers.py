"""In here we will have the controllers for the transactions.

So things like creating a new income, expense, budget, etc. will be done here.

E.g. we will need routes for creating/modifying budgets, and a page for viewing transactions.
"""
import json

from flask import Blueprint, render_template, session

from auth.controllers import login_required
from core.extensions import redis_cache

from .services import create_budget_summary

transactions_blueprint = Blueprint('transactions', __name__)


@transactions_blueprint.route('/dashboard', methods=['GET'])
@login_required
def dashboard_serve() -> str:
    """Serve `dashboard.html` page."""
    cached_user_data = json.loads(redis_cache.get(f"user:{session['user_id']}"))
    return render_template('dashboard.html',
                           user_alias=session["user_alias"],
                           transactions=cached_user_data["user_expenses"],
                           budget_summary=create_budget_summary(session["user_id"]))
