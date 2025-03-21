from typing import Final

import backend.services.auth_services

# Patch out @login_required deco, we're not testing auth
backend.services.auth_services.login_required = lambda f: f

import pytest

# budgets_blueprint will now import the patched @login_requried
from backend.routes.budget_routes import budgets_blueprint
from backend.routes.test.utils import DummyDBUser, sim_get_cache_field_miss
from flask import Flask, g


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(budgets_blueprint)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


PREFIX: Final[str] = "backend.routes.budget_routes"


#####################
# /api/budgets/load #
#####################


def test_load_budgets_cache_hit(app, client, monkeypatch):
    """Test that when cached user data is available, the endpoint returns the cached budgets."""
    with app.app_context():
        g.user_id = "test_userid"  # patch in a value for the Flask session

        # Setup return data for a cache hit
        dummy_cached_user_budgets = [
            {
                "id": "testid",
                "user_id": "test_userid",
                "category": "testcategory",
                "frequency": "testfreq",
                "amount": "testamount",
                "spent": "testspent",
                "remaining": "testremaining",
            }
        ]

        # Patch in the data to the call
        monkeypatch.setattr(
            "backend.routes.budget_routes.get_user_cache_field",
            lambda user_id, field: dummy_cached_user_budgets,
        )

        response = client.get("/api/budgets/load")
        assert response.status_code == 200

        data = response.get_json()
        assert data == dummy_cached_user_budgets


def test_load_budgets_no_cache_db_success(app, client, monkeypatch):
    """Test the case where there is no cached data, but the database returns valid user data."""
    with app.app_context():
        g.user_id = "test_userid"  # patch in a value for the Flask session

        sim_get_cache_field_miss(monkeypatch=monkeypatch, prefix=PREFIX)

        # Simulate a successful DB query.
        monkeypatch.setattr(
            "backend.routes.budget_routes.get_user_with_associations",
            lambda user_id: DummyDBUser(),
        )

        # Given we hit the db, we now simulate caching it
        monkeypatch.setattr(
            "backend.routes.budget_routes.cache_user_with_associations",
            lambda user_data: None,
        )

        response = client.get("/api/budgets/load")
        assert response.status_code == 200

        data = response.get_json()
        assert data == [{}, {}]  # Returns the budget field of the user dict


def test_load_budgets_no_cache_db_fail(app, client, monkeypatch):
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_cache_field_miss(monkeypatch, prefix=PREFIX)

        # Sim get_user_with_associations fail
        monkeypatch.setattr(
            "backend.routes.budget_routes.get_user_with_associations",
            lambda user_id: None,
        )

        response = client.get("/api/budgets/load")
        assert response.status_code == 404

        data = response.get_json()
        assert data["success"] == False
        assert data["message"] == "No cache hit then error fetching user data from db."
