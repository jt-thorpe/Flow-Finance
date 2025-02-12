from itertools import chain

from auth.controllers import login_required
from flask import Blueprint, jsonify, request
from transactions.models import Expense, Income

transactions_blueprint = Blueprint('transactions', __name__, url_prefix='/api/transactions')


@transactions_blueprint.route("/get-by", methods=["GET"])
@login_required
def get_transactions():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 20, type=int)

    # Fetch income and expenses
    incomes = Income.query.order_by(Income.date.desc()).paginate(page=page, per_page=per_page // 2, error_out=False)
    expenses = Expense.query.order_by(Expense.date.desc()).paginate(page=page, per_page=per_page // 2, error_out=False)

    # Convert to dictionary and add type tags
    income_list = [dict(tx.to_dict(), type="income") for tx in incomes.items]
    expense_list = [dict(tx.to_dict(), type="expense") for tx in expenses.items]

    # Merge and sort transactions
    transactions_combined = sorted(chain(income_list, expense_list), key=lambda x: x["date"], reverse=True)

    return jsonify({
        "transactions": transactions_combined,
        "has_more": incomes.has_next or expenses.has_next
    })
