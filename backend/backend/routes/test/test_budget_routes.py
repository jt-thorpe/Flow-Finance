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
    """Create a Flask test application with the budgets blueprint registered."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(budgets_blueprint)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


PREFIX: Final[str] = "backend.routes.budget_routes"


class TestLoadBudgetsEndpoint:
    """Test suite for the /api/budgets/load endpoint.
    
    Tests the following response scenarios:
    - 200: Successful budget load from cache or database
    - 401: Missing user authentication
    - 404: No budget data found for user
    - 500: Internal server errors (unexpected errors, malformed data, DB connection issues)
    
    Verifies both success and error response formats, including:
    - Success: {"success": true, "message": str, "budgets": list[dict]}
    - Error: {"success": false, "message": str}
    """

    def test_load_budgets_cache_hit(self, app, client, monkeypatch):
        """Test successful budget load from cache."""
        with app.app_context():
            g.user_id = "test_userid"

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

            # Mock cache hit
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_cache_field",
                lambda user_id, field: dummy_cached_user_budgets,
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 200
            data = response.get_json()
            assert data == {
                "success": True,
                "message": "Budgets loaded from cache",
                "budgets": dummy_cached_user_budgets
            }

    def test_load_budgets_no_cache_db_success(self, app, client, monkeypatch):
        """Test successful budget load from database when cache misses."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock cache miss
            sim_get_cache_field_miss(monkeypatch=monkeypatch, prefix=PREFIX)

            # Mock successful DB query
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_with_associations",
                lambda user_id: DummyDBUser(),
            )

            # Mock successful cache update
            monkeypatch.setattr(
                "backend.routes.budget_routes.cache_user_with_associations",
                lambda user_data: None,
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 200
            data = response.get_json()
            assert data == {
                "success": True,
                "message": "Budgets loaded from database",
                "budgets": [{}, {}]  # Returns the budget field of the user dict
            }

    def test_load_budgets_no_cache_db_fail(self, app, client, monkeypatch):
        """Test 404 when no budget data found in database."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock cache miss
            sim_get_cache_field_miss(monkeypatch, prefix=PREFIX)

            # Mock DB query returning no data
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_with_associations",
                lambda user_id: None,
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 404
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "No budget data found for user"
            }

    def test_load_budgets_cache_error(self, app, client, monkeypatch):
        """Test successful budget load despite cache update failure."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock cache miss
            sim_get_cache_field_miss(monkeypatch, prefix=PREFIX)

            # Mock successful DB query
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_with_associations",
                lambda user_id: DummyDBUser(),
            )

            # Mock cache update failure
            def raise_cache_error(user_data):
                raise Exception("Cache error")
                
            monkeypatch.setattr(
                "backend.routes.budget_routes.cache_user_with_associations",
                raise_cache_error,
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 200
            data = response.get_json()
            assert data == {
                "success": True,
                "message": "Budgets loaded from database",
                "budgets": [{}, {}]
            }

    def test_load_budgets_unexpected_error(self, app, client, monkeypatch):
        """Test 500 when unexpected error occurs."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock unexpected error
            def raise_unexpected_error(user_id, field):
                raise Exception("Unexpected error")
                
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_cache_field",
                raise_unexpected_error,
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 500
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "Internal server error while loading budgets"
            }

    def test_load_budgets_missing_user_id(self, app, client):
        """Test 401 when user is not authenticated (no user_id in g)."""
        with app.app_context():
            # Don't set g.user_id to simulate unauthenticated request
            response = client.get("/api/budgets/load")
            assert response.status_code == 401
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "Authentication required"
            }

    def test_load_budgets_malformed_cache_data(self, app, client, monkeypatch):
        """Test handling of malformed data in cache."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock cache hit with malformed data
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_cache_field",
                lambda user_id, field: "not_a_list",  # Should be a list of budgets
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 500
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "Internal server error while loading budgets"
            }

    def test_load_budgets_db_connection_error(self, app, client, monkeypatch):
        """Test handling of database connection errors."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock cache miss
            sim_get_cache_field_miss(monkeypatch, prefix=PREFIX)

            # Mock database connection error
            def raise_db_error(user_id):
                raise Exception("Database connection failed")
                
            monkeypatch.setattr(
                "backend.routes.budget_routes.get_user_with_associations",
                raise_db_error,
            )

            response = client.get("/api/budgets/load")
            assert response.status_code == 500
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "Internal server error while loading budgets"
            }
