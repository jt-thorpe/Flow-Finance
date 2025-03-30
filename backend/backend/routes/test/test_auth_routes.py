from datetime import datetime

import jwt
import pytest
from flask import Flask

from ...routes.auth_routes import auth_blueprint


@pytest.fixture
def app():
    """Create a Flask test application with the auth blueprint registered."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(auth_blueprint)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


class TestLoginEndpoint:
    """Test suite for the /api/auth/login endpoint."""

    def test_login_missing_fields(self, client):
        """Test login fails when email and password are missing."""
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["message"] == "Missing email or password"

    def test_login_malformed_json(self, client):
        """Test login fails when request body is not valid JSON."""
        response = client.post(
            "/api/auth/login", data="invalid json", content_type="application/json"
        )
        assert response.status_code == 400

    def test_login_wrong_content_type(self, client):
        """Test login fails when content type is not application/json."""
        response = client.post(
            "/api/auth/login",
            data="email=test@example.com&password=test",
            content_type="application/x-www-form-urlencoded",
        )
        assert response.status_code == 415

    def test_login_invalid_credentials(self, client, monkeypatch):
        """Test login fails with incorrect credentials."""
        monkeypatch.setattr(
            "backend.routes.auth_routes.authenticate", lambda email, password: False
        )

        response = client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
        assert data["message"] == "Invalid credentials"

    def test_login_success(self, client, monkeypatch):
        """Test successful login with valid credentials."""
        # Set up test data
        fake_user_id = "user123"
        fake_token = "faketoken"
        fake_expiry = 9999999999

        # Mock authentication and token generation
        def fake_authenticate(email, password):
            from flask import g

            g.user_id = fake_user_id
            return True

        monkeypatch.setattr(
            "backend.routes.auth_routes.authenticate", fake_authenticate
        )
        monkeypatch.setattr(
            "backend.routes.auth_routes.generate_token",
            lambda user_id: (fake_token, fake_expiry),
        )

        # Test login
        response = client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "correctpass"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Login successful"
        assert data["user_id"] == fake_user_id
        assert data["expires_at"] == fake_expiry

        # Verify cookie
        set_cookie = response.headers.get("Set-Cookie")
        assert "jwt=" in set_cookie
        assert fake_token in set_cookie

    def test_login_empty_strings(self, client):
        """Test login fails when email or password are empty strings."""
        response = client.post("/api/auth/login", json={"email": "", "password": ""})
        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False
        assert data["message"] == "Missing email or password"

    def test_login_cookie_security(self, client, monkeypatch):
        """Test JWT cookie has required security attributes."""

        # Mock authentication
        def fake_authenticate(email, password):
            from flask import g

            g.user_id = "test_user"
            return True

        monkeypatch.setattr(
            "backend.routes.auth_routes.authenticate", fake_authenticate
        )
        monkeypatch.setattr(
            "backend.routes.auth_routes.generate_token",
            lambda user_id: ("faketoken", 9999999999),
        )

        # Test login and verify cookie security
        response = client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "testpass"},
        )

        set_cookie = response.headers.get("Set-Cookie")
        assert "secure" in set_cookie.lower()
        assert "httponly" in set_cookie.lower()
        assert "samesite=none" in set_cookie.lower()


class TestLogoutEndpoint:
    """Test suite for the /api/auth/logout endpoint."""

    def test_logout_success(self, client):
        """Test successful logout clears the JWT cookie."""
        response = client.post("/api/auth/logout")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {"success": True, "message": "Logged out successfully"}

        # Verify cookie is cleared
        set_cookie = response.headers.get("Set-Cookie")
        assert "jwt=" in set_cookie
        assert "Expires=Thu, 01 Jan 1970 00:00:00 GMT" in set_cookie


class TestVerifyEndpoint:
    """Test suite for the /api/auth/verify endpoint."""

    def test_verify_no_token(self, client):
        """Test verification fails when no token is provided."""
        response = client.get("/api/auth/verify")
        assert response.status_code == 401
        data = response.get_json()
        assert data == {"success": False, "message": "No token provided."}

    def test_verify_token_expired(self, client, monkeypatch):
        """Test verification fails with an expired token."""

        def fake_verify_token(token):
            raise jwt.ExpiredSignatureError("JWT signature expired")

        monkeypatch.setattr(
            "backend.routes.auth_routes.verify_token", fake_verify_token
        )

        with client:
            client.set_cookie(key="jwt", value="expiredtoken", expires=datetime.now())
            response = client.get("/api/auth/verify")
        assert response.status_code == 401
        data = response.get_json()
        assert data == {"success": False, "message": "Token expired."}

    def test_verify_token_invalid(self, client, monkeypatch):
        """Test verification fails with an invalid token."""

        def fake_verify_token(token):
            raise jwt.InvalidTokenError("JWT is invalid")

        monkeypatch.setattr(
            "backend.routes.auth_routes.verify_token", fake_verify_token
        )

        with client:
            client.set_cookie(key="jwt", value="invalidtoken", expires=datetime.now())
            response = client.get("/api/auth/verify")
        assert response.status_code == 401
        data = response.get_json()
        assert data == {"success": False, "message": "Invalid token."}

    def test_verify_success(self, client, monkeypatch):
        """Test successful token verification."""
        fake_user_id = "user123"
        monkeypatch.setattr(
            "backend.routes.auth_routes.verify_token", lambda token: fake_user_id
        )

        with client:
            client.set_cookie(key="jwt", value="validtoken", expires=datetime.now())
            response = client.get("/api/auth/verify")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Token verified successfully",
            "user_id": fake_user_id,
        }

    def test_verify_token_from_header(self, client, monkeypatch):
        """Test verification works with token from Authorization header."""
        fake_user_id = "user123"
        monkeypatch.setattr(
            "backend.routes.auth_routes.verify_token", lambda token: fake_user_id
        )

        response = client.get(
            "/api/auth/verify", headers={"Authorization": "Bearer validtoken"}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Token verified successfully",
            "user_id": fake_user_id,
        }

    def test_verify_token_precedence(self, client, monkeypatch):
        """Test header token takes precedence over cookie token."""
        fake_user_id = "header_user"
        monkeypatch.setattr(
            "backend.routes.auth_routes.verify_token", lambda token: fake_user_id
        )

        with client:
            client.set_cookie(key="jwt", value="cookie_token")
            response = client.get(
                "/api/auth/verify", headers={"Authorization": "Bearer header_token"}
            )
        assert response.status_code == 200
        data = response.get_json()
        assert data["user_id"] == fake_user_id


def test_complete_auth_flow(client, monkeypatch):
    """Test the complete authentication flow: login -> verify -> logout."""
    # Set up test data
    fake_user_id = "test_user"
    fake_token = "test_token"
    fake_expiry = 9999999999

    # Mock authentication and token generation
    def fake_authenticate(email, password):
        from flask import g

        g.user_id = fake_user_id
        return True

    monkeypatch.setattr("backend.routes.auth_routes.authenticate", fake_authenticate)
    monkeypatch.setattr(
        "backend.routes.auth_routes.generate_token",
        lambda user_id: (fake_token, fake_expiry),
    )
    monkeypatch.setattr(
        "backend.routes.auth_routes.verify_token", lambda token: fake_user_id
    )

    # Test login
    response = client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["user_id"] == fake_user_id

    # Test verify
    with client:
        client.set_cookie(key="jwt", value=fake_token)
        response = client.get("/api/auth/verify")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["user_id"] == fake_user_id

    # Test logout
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
