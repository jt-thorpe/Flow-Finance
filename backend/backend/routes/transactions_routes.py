from backend.queries.transactions_queries import get_all_transactions
from backend.services.auth_services import login_required
from backend.services.cache_services import get_user_cache_field
from backend.services.transactions_services import paginate_transactions
from flask import Blueprint, g, jsonify, request

transactions_blueprint = Blueprint(
    "transactions", __name__, url_prefix="/api/transactions"
)


@transactions_blueprint.route("/list", methods=["GET"])
@login_required
def list_transactions():
    """
    Retrieve paginated transactions for the authenticated user.
    
    Attempts to fetch transactions from cache first, falling back to database if not found.
    Returns paginated results with transaction data and pagination metadata.
    
    Query Parameters:
        page (int): The page number to retrieve (default: 1)
        limit (int): Number of transactions per page (default: 20)
    
    Returns:
        tuple: (Response, int) containing:
            - JSON response with transaction data and pagination info
            - HTTP status code (200 for success, 400 for invalid params, 500 for errors)
    """
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)

    # Validate pagination parameters
    if page < 1 or limit < 1:
        return (
            jsonify({"success": False, "message": "Invalid page or limit."}),
            400,
        )

    # Try to get transactions from cache first
    cached_transactions = get_user_cache_field(user_id=g.user_id, field="transactions")

    # If cache miss, fetch from database
    if cached_transactions is None:
        transactions_list = get_all_transactions(g.user_id)
    else:
        transactions_list = cached_transactions

    # Paginate the results
    try:
        result = paginate_transactions(transactions_list, page, limit)
        return jsonify({"success": True, "data": result}), 200
    except ValueError:
        return (
            jsonify({"success": False, "message": "Unable to load transactions."}),
            500,
        )
