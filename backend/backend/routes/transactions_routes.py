from flask import Blueprint, jsonify, request

from backend.models.transaction_models import Transaction
from backend.routes.auth_routes import login_required

transactions_blueprint = Blueprint('transactions', __name__, url_prefix='/api/transactions')


@transactions_blueprint.route("/get-by", methods=["GET"])
@login_required
def get_transactions():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("limit", 20, type=int)

    transactions_query = Transaction.query.order_by(Transaction.date.desc())
    transactions_paginated = transactions_query.paginate(page=page, per_page=per_page, error_out=False)

    transactions_list = [tx.to_dict() for tx in transactions_paginated.items]

    return jsonify({
        "transactions": transactions_list,
        "has_more": transactions_paginated.has_next
    })
