from auth.controllers import login_required
from cache.services import cache_user_with_associations, get_user_cache
from flask import Blueprint, Response, g, jsonify
from users.services import get_user_with_associations

budgets_blueprint = Blueprint('budgets', __name__, url_prefix='/api/budgets')


@budgets_blueprint.route('/load', methods=['GET'])
@login_required
def load_budgets() -> tuple[Response, int]:
    """Load the budget data."""
    user_id = g.user_id
    user_data = get_user_cache(user_id)

    if not user_data:
        user_data = get_user_with_associations(user_id=user_id)

        if not user_data:
            return jsonify({'success': False, 'message': f"{__name__} - Error fetching user data from db."}), 404

        cache_user_with_associations(user_data)
        user_data = user_data.to_dict()

    print(f"{__name__} - budget dashboard data = {user_data["budgets"]}")

    return jsonify(user_data["budgets"]), 200
