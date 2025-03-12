from backend.routes.auth_routes import login_required
from backend.services.cache_services import (cache_user_with_associations,
                                             get_user_cache)
from backend.services.dashboard_services import compute_dashboard
from backend.services.users_services import get_user_with_associations
from flask import Blueprint, Response, g, jsonify

dashboard_blueprint = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard_blueprint.route('/load', methods=['GET'])
@login_required
def load_dashboard() -> tuple[Response, int]:
    """Return the data required by the /dashboard page.

    If unable to load data from cache, hits the db and caches the user information. We then compute figures for the frontend.
    """
    user_id = g.user_id
    user_data = get_user_cache(user_id)

    if not user_data:
        user_data = get_user_with_associations(user_id=user_id)

        if not user_data:
            return jsonify({'success': False, 'message': f"{__name__} - Error fetching user data from db."}), 404

        cache_user_with_associations(user_data)
        user_data = user_data.to_dict()

    print("dashboard_routes.load_dashboard : user_data returned from cache")
    computed_dashboard_data = compute_dashboard(user_data=user_data)

    return jsonify(computed_dashboard_data), 200
