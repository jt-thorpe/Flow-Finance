import backend.services.auth_services
from backend.routes.test.utils import (
    DummyDashboardData,
    DummyDBUser,
    sim_add_log_critical,
    sim_add_log_error,
    sim_cache_user_with_associations_fail,
    sim_cache_user_with_associations_success,
    sim_compute_dashboard_fail,
    sim_compute_dashboard_success,
    sim_get_user_cache_hit,
    sim_get_user_cache_miss,
    sim_get_user_with_associations_hit,
    sim_get_user_with_associations_miss,
)

# Patch out @login_required deco, we're not testing auth
backend.services.auth_services.login_required = lambda f: f

from typing import Final

import pytest
from backend.routes.dashboard_routes import dashboard_blueprint
from flask import Flask, g


@pytest.fixture
def app():
    """Create a Flask test application with the dashboard blueprint registered."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(dashboard_blueprint)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


PREFIX: Final[str] = "backend.routes.dashboard_routes"


class TestLoadDashboardEndpoint:
    """Test suite for the /api/dashboard/load endpoint.

    Tests the following response scenarios:
    - 200: Successful dashboard load from cache or database
    - 401: Missing user authentication
    - 404: No user data found
    - 500: Internal server errors (cache errors, computation errors)

    Verifies both success and error response formats, including:
    - Success: Complete dashboard data structure
    - Error: {"success": false, "message": str}
    """

    def test_load_dashboard_missing_user_id(self, app, client):
        """Test 401 when user is not authenticated (no user_id in g)."""
        with app.app_context():
            # Don't set g.user_id to simulate unauthenticated request
            response = client.get("/api/dashboard/load")
            assert response.status_code == 401
            data = response.get_json()
            assert data == {"success": False, "message": "Authentication required"}

    def test_load_dashboard_cache_hit_success(self, app, client, monkeypatch):
        """Test successful dashboard load from cache."""
        with app.app_context():
            g.user_id = "test_userid"
            test_user = DummyDBUser().to_dict()
            test_data = DummyDashboardData().to_dict()

            # Mock successful cache hit
            sim_get_user_cache_hit(monkeypatch, prefix=PREFIX, data=test_user)
            sim_compute_dashboard_success(monkeypatch, prefix=PREFIX, data=test_data)

            response = client.get("/api/dashboard/load")
            assert response.status_code == 200
            assert response.get_json() == test_data

    def test_load_dashboard_cache_hit_compute_fail(self, app, client, monkeypatch):
        """Test 500 when dashboard computation fails with cached data."""
        with app.app_context():
            g.user_id = "test_userid"
            test_user = DummyDBUser().to_dict()

            # Mock cache hit but computation failure
            sim_get_user_cache_hit(monkeypatch, prefix=PREFIX, data=test_user)
            sim_compute_dashboard_fail(monkeypatch, prefix=PREFIX)
            sim_add_log_error(monkeypatch, prefix=PREFIX)

            response = client.get("/api/dashboard/load")
            assert response.status_code == 500
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "Error computing dashboard data",
            }

    def test_load_dashboard_cache_db_miss(self, app, client, monkeypatch):
        """Test 404 when no data found in cache or database."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock both cache and DB miss
            sim_get_user_cache_miss(monkeypatch, prefix=PREFIX)
            sim_get_user_with_associations_miss(monkeypatch, prefix=PREFIX)

            response = client.get("/api/dashboard/load")
            assert response.status_code == 404
            data = response.get_json()
            assert data == {"success": False, "message": "No user data found"}

    def test_load_dashboard_cache_miss_db_hit_cache_fail(
        self, app, client, monkeypatch
    ):
        """Test 500 when cache update fails after DB hit."""
        with app.app_context():
            g.user_id = "test_userid"

            # Mock cache miss but DB hit
            sim_get_user_cache_miss(monkeypatch, prefix=PREFIX)
            sim_get_user_with_associations_hit(
                monkeypatch, prefix=PREFIX, data=DummyDBUser()
            )

            # Mock cache update failure
            sim_cache_user_with_associations_fail(monkeypatch, prefix=PREFIX)
            sim_add_log_critical(monkeypatch, prefix=PREFIX)

            response = client.get("/api/dashboard/load")
            assert response.status_code == 500
            data = response.get_json()
            assert data == {"success": False, "message": "Error loading dashboard data"}

    def test_load_dashboard_cache_miss_db_hit_success(self, app, client, monkeypatch):
        """Test successful dashboard load from database with cache update."""
        with app.app_context():
            g.user_id = "test_userid"
            test_user = DummyDBUser()
            test_data = DummyDashboardData().to_dict()

            # Mock cache miss but successful DB and cache flow
            sim_get_user_cache_miss(monkeypatch, prefix=PREFIX)
            sim_get_user_with_associations_hit(
                monkeypatch, prefix=PREFIX, data=test_user
            )
            sim_cache_user_with_associations_success(monkeypatch, prefix=PREFIX)
            sim_compute_dashboard_success(monkeypatch, prefix=PREFIX, data=test_data)

            response = client.get("/api/dashboard/load")
            assert response.status_code == 200
            assert response.get_json() == test_data

    def test_load_dashboard_cache_miss_db_hit_compute_fail(
        self, app, client, monkeypatch
    ):
        """Test 500 when dashboard computation fails with database data."""
        with app.app_context():
            g.user_id = "test_userid"
            test_user = DummyDBUser()

            # Mock successful DB flow but computation failure
            sim_get_user_cache_miss(monkeypatch, prefix=PREFIX)
            sim_get_user_with_associations_hit(
                monkeypatch, prefix=PREFIX, data=test_user
            )
            sim_cache_user_with_associations_success(monkeypatch, prefix=PREFIX)
            sim_compute_dashboard_fail(monkeypatch, prefix=PREFIX)
            sim_add_log_error(monkeypatch, prefix=PREFIX)

            response = client.get("/api/dashboard/load")
            assert response.status_code == 500
            data = response.get_json()
            assert data == {
                "success": False,
                "message": "Error computing dashboard data",
            }
