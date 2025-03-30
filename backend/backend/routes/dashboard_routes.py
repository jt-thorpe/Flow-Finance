from backend.extensions import logger
from backend.services.auth_services import login_required
from backend.services.cache_services import cache_user_with_associations, get_user_cache
from backend.services.dashboard_services import compute_dashboard
from backend.services.users_services import get_user_with_associations
from flask import Blueprint, Response, g, jsonify

dashboard_blueprint = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_blueprint.route("/load", methods=["GET"])
@login_required
def load_dashboard() -> tuple[Response, int]:
    """
    Load and compute dashboard data for the authenticated user.

    Retrieves user data from cache or database, then computes dashboard metrics.

    Returns:
        tuple[Response, int]: (response, status_code)
            - 200: Success with dashboard data
            - 401: User not authenticated
            - 404: Data not found or computation failed
            - 500: Internal server error

    Response Format:
        Success (200):
            {
                "user_alias": str,
                "user_latest_transactions": list[dict],
                "user_incomes_total": list[int],
                "user_expenses_total": list[int],
                "user_budget_summary": list[dict]
            }
        Error (401/404/500):
            {
                "success": false,
                "message": str
            }
    """
    try:
        if not hasattr(g, "user_id"):
            logger.error(
                "dashboard_routes.load_dashboard : No user_id in request context"
            )
            return (
                jsonify({"success": False, "message": "Authentication required"}),
                401,
            )

        user_id = g.user_id
        logger.info(
            f"dashboard_routes.load_dashboard : Loading dashboard for user {user_id}"
        )

        user_data = get_user_cache(user_id)

        if not user_data:
            logger.info(
                f"dashboard_routes.load_dashboard : Cache miss for user {user_id}, querying database"
            )
            user_data = get_user_with_associations(user_id=user_id)

            if not user_data:
                logger.error(
                    f"dashboard_routes.load_dashboard : No data found for user {user_id}"
                )
                return jsonify({"success": False, "message": "No user data found"}), 404

            try:
                cache_user_with_associations(user_data)
                user_data = user_data.to_dict()
                logger.info(
                    f"dashboard_routes.load_dashboard : Successfully cached user data for {user_id}"
                )
            except Exception as e:
                logger.error(
                    f"dashboard_routes.load_dashboard : Cache error for user {user_id}: {str(e)}"
                )
                return (
                    jsonify(
                        {"success": False, "message": "Error loading dashboard data"}
                    ),
                    500,
                )

        try:
            computed_dashboard_data = compute_dashboard(user_data=user_data)
            logger.info(
                f"dashboard_routes.load_dashboard : Successfully computed dashboard for user {user_id}"
            )
            return jsonify(computed_dashboard_data), 200
        except Exception as e:
            logger.error(
                f"dashboard_routes.load_dashboard : Computation error for user {user_id}: {str(e)}"
            )
            return (
                jsonify(
                    {"success": False, "message": "Error computing dashboard data"}
                ),
                500,
            )

    except Exception as e:
        logger.error(
            f"dashboard_routes.load_dashboard : Unexpected error: {str(e)}",
            exc_info=True,
        )
        return jsonify({"success": False, "message": "Internal server error"}), 500
