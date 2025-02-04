from auth.controllers import login_required
from cache.services import cache_user_with_associations, get_user_cache
from flask import Blueprint, Response, jsonify, request
from users.services import (get_user_with_associations,
                            serialise_user_associations)

users_blueprint = Blueprint('users', __name__, url_prefix='/api/users')


@users_blueprint.route('/me', methods=['GET'])
@login_required
def get_user_data() -> tuple[Response, int]:
    """Retrieve user data from cache or database."""
    user_id = request.user_id  # Extracted from JWT, not sure this is right...

    # Check Redis cache first
    user_data = get_user_cache(user_id=user_id)

    print(f"{__name__} - user_data from cache = {user_data}")

    if not user_data:
        # If not cached, fetch from the database
        # this gives is Python objects, unserialised for redis or sending frontend
        user_data = get_user_with_associations(user_id=user_id)
        print(f"{__name__} - user_data from db = {user_data}")

        if not user_data:
            return jsonify({'success': False, 'message': 'User not found'}), 404

        # Store in Redis for future requests
        cache_user_with_associations(user_data)
        # This serialisation needs to be done earlier, somewhere else, otherwise we're going to be serialising it all over the place...
        user_data = serialise_user_associations(user_data)

    return jsonify({'success': True, 'user': user_data}), 200
