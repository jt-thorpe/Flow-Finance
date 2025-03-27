from backend.services.auth_services import login_required
from backend.services.cache_services import (
    cache_user_with_associations,
    get_user_cache_field,
)
from backend.services.users_services import get_user_with_associations
from backend.extensions import logger
from flask import Blueprint, Response, g, jsonify

budgets_blueprint = Blueprint("budgets", __name__, url_prefix="/api/budgets")


@budgets_blueprint.route("/load", methods=["GET"])
@login_required
def load_budgets() -> tuple[Response, int]:
    """
    Load the user's budget data.
    
    Attempts to retrieve budget data from cache first, falling back to database if needed.
    Caches database results for future requests.
    
    Returns:
        tuple: (Response, int) containing:
            - JSON response with budget data and status
            - HTTP status code (200 for success, 404 for not found, 500 for errors)
    """
    try:
        user_id = g.user_id
        cached_user_budgets = get_user_cache_field(user_id=user_id, field="budgets")

        if cached_user_budgets:
            logger.info(f"budget_routes.load_budgets : Cache hit for user {user_id}")
            return jsonify({
                "success": True,
                "message": "Budgets loaded from cache",
                "budgets": cached_user_budgets
            }), 200

        logger.info(f"budget_routes.load_budgets : Cache miss for user {user_id}, querying database")
        user_data = get_user_with_associations(user_id=user_id)

        if not user_data:
            logger.error(f"budget_routes.load_budgets : No data found for user {user_id}")
            return jsonify({
                "success": False,
                "message": "No budget data found for user"
            }), 404

        try:
            cache_user_with_associations(user_data)
            logger.info(f"budget_routes.load_budgets : Cached user data for {user_id}")
        except Exception as cache_error:
            logger.error(f"budget_routes.load_budgets : Cache error for user {user_id}: {str(cache_error)}")
            # Continue execution as we still have the data to return

        user_data = user_data.to_dict()
        return jsonify({
            "success": True,
            "message": "Budgets loaded from database",
            "budgets": user_data["budgets"]
        }), 200

    except Exception as e:
        logger.error(f"budget_routes.load_budgets : Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Internal server error while loading budgets"
        }), 500
