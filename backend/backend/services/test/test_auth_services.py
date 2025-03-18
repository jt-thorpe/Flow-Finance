from datetime import datetime

import jwt
import pytest
from flask import Flask, jsonify

from ...routes.auth_routes import auth_blueprint
from ..auth_services import login_required


# Create a simple Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    # Dummy protected route to test login_required decorator
    @app.route("/protected")
    @login_required
    def protected():
        return jsonify({"auth": True, "message": "Route access authorised."}), 200

    return app


@pytest.fixture
def client(app):
    return app.test_client()


###################
# @login_required #
###################


def test_login_requried_no_token(client):
    # Accessing a protected route without a token should result in 401
    response = client.get("/protected")
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "No token present."


def test_login_requried_no_user_id(client, monkeypatch):
    def empty_verify_token(token):
        """Simulates verify_token returning an empty string."""
        return ""

    monkeypatch.setattr("backend.services.auth_services.verify_token", empty_verify_token)

    client.set_cookie(key="jwt", value="validtoken", expires=datetime.now())
    response = client.get("/protected")
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "Bad authentication."


def test_login_requried_expired_token(client, monkeypatch):
    def expired_verify_token(token):
        raise jwt.ExpiredSignatureError()

    monkeypatch.setattr("backend.services.auth_services.verify_token", expired_verify_token)

    with client:
        client.set_cookie(key="jwt", value="expiredtoken", expires=datetime.now())
        response = client.get('/protected')
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "Session expired."


def test_login_requried_invalid_token(client, monkeypatch):
    def invalid_verify_token(token):
        raise jwt.InvalidSignatureError()

    monkeypatch.setattr("backend.services.auth_services.verify_token", invalid_verify_token)

    with client:
        client.set_cookie(key="jwt", value="invalidtoken", expires=datetime.now())
        response = client.get('/protected')
    assert response.status_code == 401

    data = response.get_json()
    assert data["auth"] == False
    assert data["message"] == "Invalid token."


def test_protected_route_valid_token(client, monkeypatch):
    fake_user_id = "user123"
    monkeypatch.setattr("backend.services.auth_services.verify_token", lambda token: fake_user_id)

    with client:
        client.set_cookie(key="jwt", value="validtoken", expires=datetime.now())
        response = client.get("/protected")
    assert response.status_code == 200

    data = response.get_json()
    assert data["auth"] == True
    assert data["message"] == "Route access authorised."
