from sys import prefix
from typing import Final
from urllib import response

import backend.services.auth_services

# Patch out @login_required deco, we're not testing auth
backend.services.auth_services.login_required = lambda f: f

import pytest
from backend.routes.test.utils import (
    DummyDBUser,
    sim_cache_user_with_associations_success,
    sim_get_cache_field_miss,
    sim_get_user_cache_hit,
    sim_get_user_cache_miss,
    sim_get_user_with_associations_hit,
    sim_get_user_with_associations_miss,
    sim_serialise_user_associations_success,
)

# blueprint will now import the patched @login_requried
from backend.routes.users_routes import users_blueprint
from flask import Flask, g


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(users_blueprint)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


FUNC_PREFIX: Final[str] = "backend.routes.users_routes"


#################
# /api/users/me #
#################


def test_get_user_data_cache_hit(app, client, monkeypatch):
    with app.app_context():
        g.user_id = "test_userid"
        test_user = DummyDBUser().to_dict()

        sim_get_user_cache_hit(
            monkeypatch,
            prefix=FUNC_PREFIX,
            data=test_user,
        )

        response = client.get("/api/users/me")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] == True
        assert data["user"] == test_user


def test_get_user_data_cache_miss_db_miss(app, client, monkeypatch):
    """Test the case where there is no data in the cache and we fail to retreive from the db."""
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_user_cache_miss(monkeypatch, prefix=FUNC_PREFIX)

        sim_get_user_with_associations_miss(monkeypatch, prefix=FUNC_PREFIX)

        response = client.get("/api/users/me")
        assert response.status_code == 404

        data = response.get_json()
        assert data["success"] == False
        assert data["message"] == "User not found."


def test_get_user_data_cache_miss_db_hit(app, client, monkeypatch):
    """Simualte the case where there is no data in the cache but we successfully hit the db."""
    with app.app_context():
        g.user_id = "test_userid"
        test_user = DummyDBUser().to_dict()

        sim_get_user_cache_miss(monkeypatch, prefix=FUNC_PREFIX)

        sim_get_user_with_associations_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=test_user
        )

        sim_cache_user_with_associations_success(monkeypatch, prefix=FUNC_PREFIX)

        sim_serialise_user_associations_success(
            monkeypatch, prefix=FUNC_PREFIX, data=test_user
        )

        response = client.get("/api/users/me")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] == True
        assert data["user"] == test_user
