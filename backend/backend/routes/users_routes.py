from backend.services.auth_services import hash_password, login_required
from backend.services.cache_services import cache_user_with_associations, get_user_cache
from backend.services.users_services import (
    add_user_account_to_db,
    get_user_with_associations,
    is_taken,
    serialise_user_associations,
)
from flask import Blueprint, Response, g, jsonify, request
from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint("users", __name__, url_prefix="/api/users")


@users_blueprint.route("/me", methods=["GET"])
@login_required
def get_user_data() -> tuple[Response, int]:
    """Retrieve user data from cache or database."""
    user_id = g.user_id  # Extracted from JWT, not sure this is right...

    # Check Redis cache first
    user_data = get_user_cache(user_id=user_id)

    print(f"{__name__} - user_data from cache = {user_data}")

    if not user_data:
        # If not cached, fetch from the database
        # this gives is Python objects, unserialised for redis or sending frontend
        user_data = get_user_with_associations(user_id=user_id)
        print(f"{__name__} - user_data from db = {user_data}")

        if not user_data:
            return jsonify({"success": False, "message": "User not found"}), 404

        # Store in Redis for future requests
        cache_user_with_associations(user_data)
        # This serialisation needs to be done earlier, somewhere else, otherwise we're going to be serialising it all over the place...
        user_data = serialise_user_associations(user_data)

    return jsonify({"success": True, "user": user_data}), 200


@users_blueprint.route("/check-taken", methods=["GET"])
def check_email() -> tuple[Response, int]:
    """Check if an email is already in use with a user account."""
    email = request.args.get("email")

    print(f"{__name__} - email = {email}")

    # TODO: Add err handling
    if is_taken(email=email):
        return jsonify({"success": True, "taken": True}), 200

    return jsonify({"success": True, "taken": False}), 200


@users_blueprint.route("/register", methods=["POST"])
def register_user() -> tuple[Response, int]:
    """Register the user in the database."""
    data = request.json

    alias = data["alias"]
    email = data["email"]
    h_password = hash_password(data["password"])

    try:
        add_user_account_to_db(alias=alias, email=email, hashed_password=h_password)

        return jsonify({"success": True}), 200
    except IntegrityError as e:
        print(f"{e} - unable to add user to database")
        return jsonify({"success": False}), 500
