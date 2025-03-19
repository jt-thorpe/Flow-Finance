from backend.services.auth_services import login_required
from backend.services.cache_services import (
    cache_user_with_associations,
    get_user_cache_field,
)
from backend.services.users_services import get_user_with_associations
from flask import Blueprint, Response, g, jsonify

budgets_blueprint = Blueprint("budgets", __name__, url_prefix="/api/budgets")


@budgets_blueprint.route("/load", methods=["GET"])
@login_required
def load_budgets() -> tuple[Response, int]:
    """Load the budget data."""
    user_id = g.user_id
    cached_user_budgets = get_user_cache_field(user_id=user_id, field="budgets")

    if not cached_user_budgets:
        user_data = get_user_with_associations(user_id=user_id)

        if not user_data:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "No cache hit then error fetching user data from db.",
                    }
                ),
                404,
            )

        cache_user_with_associations(user_data)
        user_data = user_data.to_dict()

        return jsonify(user_data["budgets"]), 200

    return jsonify(cached_user_budgets), 200
