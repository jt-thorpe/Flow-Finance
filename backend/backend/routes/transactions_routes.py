import json

from backend.models.transaction_models import Transaction
from backend.services.auth_services import login_required
from flask import Blueprint, jsonify, request

transactions_blueprint = Blueprint('transactions', __name__, url_prefix='/api/transactions')


@transactions_blueprint.route("/get-by", methods=["GET"])
@login_required
def get_transactions():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)

    transactions_query = Transaction.query.order_by(Transaction.date.desc())
    transactions_paginated = transactions_query.paginate(page=page, per_page=limit, error_out=False)

    transactions_list = [tx.to_dict() for tx in transactions_paginated.items]

    print(
        f"transactions_routes.get_transaction : transactions_list = {json.dumps(transactions_list, sort_keys=True, indent=4)}")

    return jsonify({
        "transactions": transactions_list,
        "has_more": transactions_paginated.has_next
    })
