from datetime import datetime

import jwt
import pytest
from flask import Flask

from ...routes.auth_routes import auth_blueprint


# Create a simple Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(auth_blueprint)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


###################
# /api/auth/login #
###################


def test_login_missing_fields(client):
    # Missing email and password should return 400
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Missing email or password"


def test_login_invalid_credentials(client, monkeypatch):
    # Override authenticate to simulate invalid credentials (return False)
    monkeypatch.setattr(
        "backend.routes.auth_routes.authenticate", lambda email, password: False
    )

    response = client.post(
        "/api/auth/login", json={"email": "user@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    data = response.get_json()
    assert data["message"] == "Invalid credentials"


def test_login_success(client, monkeypatch):
    # Set up fake values for a successful login
    fake_user_id = "user123"
    fake_token = "faketoken"
    fake_expiry = 9999999999

    # Override authenticate to simulate a valid login and set g.user_id
    def fake_authenticate(email, password):
        from flask import g

        g.user_id = fake_user_id
        return True

    monkeypatch.setattr("backend.routes.auth_routes.authenticate", fake_authenticate)
    # Override generate_token to return our fake token and expiry
    monkeypatch.setattr(
        "backend.routes.auth_routes.generate_token",
        lambda user_id: (fake_token, fake_expiry),
    )

    response = client.post(
        "/api/auth/login", json={"email": "user@example.com", "password": "correctpass"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
    assert data["user_id"] == fake_user_id

    # Check that the jwt cookie is set correctly
    set_cookie = response.headers.get("Set-Cookie")
    assert "jwt=" in set_cookie
    assert fake_token in set_cookie


####################
# /api/auth/logout #
####################


def test_logout(client):
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Logged out"
    # Verify that the jwt cookie is cleared (cookie value empty and expires=0)
    set_cookie = response.headers.get("Set-Cookie")
    assert "jwt=" in set_cookie
    assert (
        "Expires=Thu, 01 Jan 1970 00:00:00 GMT" in set_cookie
    )  # Flask default past date


####################
# /api/auth/verify #
####################


def test_verify_no_token(client):
    # When no token is provided, the endpoint should return 401
    response = client.get("/api/auth/verify")
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "No token provided."


def test_verify_token_expired(client, monkeypatch):
    # Simulate an expired token by monkeypatching verify_token to raise an ExpiredSignatureError
    def fake_verify_token(token):
        raise jwt.ExpiredSignatureError("JWT signature expired")

    monkeypatch.setattr("backend.routes.auth_routes.verify_token", fake_verify_token)

    with client:
        client.set_cookie(key="jwt", value="expiredtoken", expires=datetime.now())
        response = client.get("/api/auth/verify")
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "Token expired."


def test_verify_token_invalid(client, monkeypatch):
    # Simulate an invalid token by monkeypatching verify_token to raise an InvalidTokenError
    def fake_verify_token(token):
        raise jwt.InvalidTokenError("JWT is invalid")

    monkeypatch.setattr("backend.routes.auth_routes.verify_token", fake_verify_token)

    with client:
        client.set_cookie(key="jwt", value="invalidtoken", expires=datetime.now())
        response = client.get("/api/auth/verify")
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "Invalid token."


def test_verify_success(client, monkeypatch):
    fake_user_id = "user123"
    # Override verify_token to return a fake user_id
    monkeypatch.setattr(
        "backend.routes.auth_routes.verify_token", lambda token: fake_user_id
    )

    with client:
        client.set_cookie(key="jwt", value="validtoken", expires=datetime.now())
        response = client.get("/api/auth/verify")
    assert response.status_code == 200

    data = response.get_json()
    assert data["auth"] is True
    assert data["user_id"] == fake_user_id
