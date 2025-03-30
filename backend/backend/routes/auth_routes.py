import jwt
from backend.extensions import logger
from backend.services.auth_services import (
    authenticate,
    generate_token,
    get_token_from_header,
    verify_token,
)
from flask import Blueprint, Response, g, jsonify, make_response, request

# Blueprint for authentication-related routes
auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_blueprint.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
    """
    Authenticate a user and create a new session.

    Request Body:
        {
            "email": str,
            "password": str
        }

    Returns:
        tuple[Response, int]: (response, status_code)
            - 200: Login successful
            - 400: Missing/empty email/password
            - 401: Invalid credentials

    Response Format:
        Success (200):
            {
                "success": true,
                "message": "Login successful",
                "user_id": str,
                "expires_at": int
            }
        Error (400/401):
            {
                "success": false,
                "message": str
            }
    """
    data = request.json
    email, password = data.get("email"), data.get("password")

    # Validate required fields
    if not email or not password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    # Attempt authentication
    if authenticate(email, password):
        # Generate JWT token and expiry time
        token, expiry = generate_token(user_id=g.user_id)

        # Prepare successful response with user data
        response = make_response(
            jsonify(
                {
                    "success": True,
                    "message": "Login successful",
                    "user_id": g.user_id,
                    "expires_at": expiry,
                }
            ),
            200,
        )

        # Set secure cookie with JWT token
        response.set_cookie(
            key="jwt",
            value=token,
            expires=expiry,
            path="/",
            secure=True,  # Only sent over HTTPS
            httponly=True,  # Not accessible via JavaScript
            samesite="None",  # Allow cross-origin requests
        )
        return response

    return jsonify({"success": False, "message": "Invalid credentials"}), 401


@auth_blueprint.route("/verify", methods=["GET"])
def verify_authenticity() -> tuple[Response, int]:
    """
    Verify the authenticity of the current session token.

    Token can be provided in:
    - Authorization header (Bearer token)
    - jwt cookie (if no Authorization header)

    Returns:
        tuple[Response, int]: (response, status_code)
            - 200: Token valid
            - 401: Token missing/expired/invalid

    Response Format:
        Success (200):
            {
                "success": true,
                "message": "Token verified successfully",
                "user_id": str
            }
        Error (401):
            {
                "success": false,
                "message": str
            }
    """
    # Try to get token from Authorization header first, fall back to cookie
    token = (
        get_token_from_header(request.headers.get("Authorization"))
        if not request.cookies
        else request.cookies.get("jwt")
    )

    logger.info(f"auth_routes.verify_authenticity : Token is {token}")

    if not token:
        logger.info("auth_routes.verify_session : No token was provided.")
        return jsonify({"success": False, "message": "No token provided."}), 401

    try:
        # Verify token signature and expiry
        user_id = verify_token(token)
    except jwt.ExpiredSignatureError:
        logger.warning(
            "auth_routes.verify_authenticity : Token is EXPIRED.", exc_info=1
        )
        return jsonify({"success": False, "message": "Token expired."}), 401
    except jwt.InvalidTokenError:
        logger.warning(
            "auth_routes.verify_authenticity : Token is INVALID.", exc_info=1
        )
        return jsonify({"success": False, "message": "Invalid token."}), 401

    logger.info("auth_routes.verify_session : Token verification successful.")
    return (
        jsonify(
            {
                "success": True,
                "message": "Token verified successfully",
                "user_id": user_id,
            }
        ),
        200,
    )


@auth_blueprint.route("/logout", methods=["POST"])
def terminate_session() -> tuple[Response, int]:
    """
    Terminate the current user session by clearing the JWT cookie.

    No authentication required. Safe to call with invalid/expired sessions.

    Returns:
        tuple[Response, int]: (response, 200)

    Response Format:
        {
            "success": true,
            "message": "Logged out successfully"
        }
    """
    response = make_response(
        jsonify({"success": True, "message": "Logged out successfully"})
    )
    # Clear the JWT cookie with secure attributes
    response.set_cookie(
        "jwt",
        "",  # Empty value
        expires=0,  # Immediate expiration
        httponly=True,
        secure=True,
        samesite=None,
        path="/",
    )
    return response, 200
