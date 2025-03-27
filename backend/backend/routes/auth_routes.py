import jwt
from backend.extensions import logger
from backend.services.auth_services import (
    authenticate,
    generate_token,
    get_token_from_header,
    verify_token,
)
from flask import Blueprint, Response, g, jsonify, make_response, request

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    email, password = data.get("email"), data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    if authenticate(email, password):
        token, expiry = generate_token(user_id=g.user_id)
        response = make_response(
            jsonify({
                "success": True,
                "message": "Login successful",
                "user_id": g.user_id,
                "expires_at": expiry
            }),
            200,
        )

        response.set_cookie(
            key="jwt",
            value=token,
            expires=expiry,
            path="/",
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response

    return jsonify({"success": False, "message": "Invalid credentials"}), 401


@auth_blueprint.route("/verify", methods=["GET"])
def verify_authenticity() -> tuple[Response, int]:
    """Verifies that the provided token is genuine."""
    token = (
        get_token_from_header(request.headers.get("Authorization"))
        if not request.cookies
        else request.cookies.get("jwt")
    )

    logger.info(f"auth_routes.verify_authenticity : Token is {token}")

    if not token:
        logger.info("auth_routes.verify_session : No token was provided.")
        return jsonify({
            "success": False,
            "message": "No token provided."
        }), 401

    try:
        user_id = verify_token(token)
    except jwt.ExpiredSignatureError:
        logger.warning(
            "auth_routes.verify_authenticity : Token is EXPIRED.", exc_info=1
        )
        return jsonify({
            "success": False,
            "message": "Token expired."
        }), 401
    except jwt.InvalidTokenError:
        logger.warning(
            "auth_routes.verify_authenticity : Token is INVALID.", exc_info=1
        )
        return jsonify({
            "success": False,
            "message": "Invalid token."
        }), 401

    logger.info("auth_routes.verify_session : Token verification successful.")
    return jsonify({
        "success": True,
        "message": "Token verified successfully",
        "user_id": user_id
    }), 200


@auth_blueprint.route("/logout", methods=["POST"])
def terminate_session() -> tuple[Response, int]:
    """
    Terminate the current user session.
    
    Invalidates the current session by clearing the JWT cookie.
    
    Returns:
        tuple: (Response, int) containing:
            - JSON response with logout confirmation
            - HTTP status code (200 for success)
    """
    response = make_response(jsonify({
        "success": True,
        "message": "Logged out successfully"
    }))
    response.set_cookie(
        "jwt", "", expires=0, httponly=True, secure=True, samesite=None, path="/"
    )
    return response, 200
