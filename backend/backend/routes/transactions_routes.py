from backend.models.transaction_models import Transaction
from backend.queries.transactions_queries import get_all_transactions
from backend.services.auth_services import login_required
from backend.services.cache_services import get_user_cache_field
from backend.services.transactions_services import paginate_transactions
from flask import Blueprint, g, jsonify, request

transactions_blueprint = Blueprint(
    "transactions", __name__, url_prefix="/api/transactions"
)


@transactions_blueprint.route("/get-by", methods=["GET"])
@login_required
def get_transactions():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)

    cached_transactions = get_user_cache_field(user_id=g.user_id, field="transactions")

    if cached_transactions is None:
        # Rethink this part; should never be no transactions at this point
        transactions_list = get_all_transactions(g.user_id)
    else:
        transactions_list = cached_transactions

    # Now paginate the list in-memory.
    result = paginate_transactions(transactions_list, page, limit)
    return jsonify(result), 200
