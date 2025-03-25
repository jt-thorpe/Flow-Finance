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
from flask.cli import F

# Patch out @login_required deco, we're not testing auth
backend.services.auth_services.login_required = lambda f: f

from typing import Final

import pytest
from backend.routes.dashboard_routes import dashboard_blueprint
from flask import Flask, g


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(dashboard_blueprint)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


FUNC_PREFIX: Final[str] = "backend.routes.dashboard_routes"


#######################
# /api/dashboard/load #
#######################


def test_load_dashboard_cache_hit_success(app, client, monkeypatch):
    """Test the case where we attempt to load the dashboard and data is already in cache."""
    with app.app_context():
        g.user_id = "test_userid"
        test_user = DummyDBUser().to_dict()

        sim_get_user_cache_hit(monkeypatch, prefix=FUNC_PREFIX, data=test_user)

        test_data = DummyDashboardData().to_dict()
        sim_compute_dashboard_success(monkeypatch, prefix=FUNC_PREFIX, data=test_data)

        resp = client.get("/api/dashboard/load")
        assert resp.status_code == 200

        data = resp.get_json()
        assert data == test_data


def test_load_dashboard_cache_hit_fail(app, client, monkeypatch):
    """Test the case where we hit the cache but fail to compute the dashboard."""
    with app.app_context():
        g.user_id = "test_userid"
        test_user = DummyDBUser().to_dict()

        sim_get_user_cache_hit(monkeypatch, prefix=FUNC_PREFIX, data=test_user)

        sim_compute_dashboard_fail(monkeypatch, prefix=FUNC_PREFIX)
        sim_add_log_error(monkeypatch, prefix=FUNC_PREFIX)

        resp = client.get("/api/dashboard/load")
        assert resp.status_code == 404

        data = resp.get_json()
        assert data["success"] == False
        assert data["message"] == "Background error. Unable to compute dashboard."


def test_load_dashboard_cache_db_miss(app, client, monkeypatch):
    """Test the case where we attempt to load the dashboard and miss on cache and db."""
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_user_cache_miss(monkeypatch, prefix=FUNC_PREFIX)

        sim_get_user_with_associations_miss(monkeypatch, prefix=FUNC_PREFIX)

        resp = client.get("/api/dashboard/load")
        assert resp.status_code == 404

        data = resp.get_json()
        assert data["success"] == False
        assert data["message"] == "Error fetching user data from db."


def test_load_dashboard_cache_miss_db_hit_cant_cache(app, client, monkeypatch):
    """Test the case where we miss on the cache and hit db."""
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_user_cache_miss(monkeypatch, prefix=FUNC_PREFIX)

        test_user = DummyDBUser().to_dict()
        sim_get_user_with_associations_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=test_user
        )

        sim_cache_user_with_associations_fail(monkeypatch, prefix=FUNC_PREFIX)
        sim_add_log_critical(monkeypatch, prefix=FUNC_PREFIX)

        resp = client.get("/api/dashboard/load")
        assert resp.status_code == 404

        data = resp.get_json()
        assert data["success"] == False
        assert data["message"] == "Background error. Unable to load dashboard."


def test_load_dashboard_cache_miss_db_hit_can_cache_can_compute(
    app, client, monkeypatch
):
    """Test the case where we miss on the cache, hit the db, cache it successfully, and compute dash info."""
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_user_cache_miss(monkeypatch, prefix=FUNC_PREFIX)

        test_user = DummyDBUser()
        sim_get_user_with_associations_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=test_user
        )

        sim_cache_user_with_associations_success(monkeypatch, prefix=FUNC_PREFIX)

        test_data = DummyDashboardData().to_dict()
        sim_compute_dashboard_success(monkeypatch, prefix=FUNC_PREFIX, data=test_data)

        resp = client.get("/api/dashboard/load")
        assert resp.status_code == 200

        data = resp.get_json()
        assert data == test_data


def test_load_dashboard_cache_miss_db_hit_can_cache_cant_compute(
    app, client, monkeypatch
):
    """Test the case where we miss on the cache, hit the db, cache it successfully, and fail to compute dashboard info."""
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_user_cache_miss(monkeypatch, prefix=FUNC_PREFIX)

        test_user = DummyDBUser()
        sim_get_user_with_associations_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=test_user
        )

        sim_cache_user_with_associations_success(monkeypatch, prefix=FUNC_PREFIX)

        sim_compute_dashboard_fail(monkeypatch, prefix=FUNC_PREFIX)
        sim_add_log_error(monkeypatch, prefix=FUNC_PREFIX)

        resp = client.get("/api/dashboard/load")
        assert resp.status_code == 404

        data = resp.get_json()
        assert data["success"] == False
        assert data["message"] == "Background error. Unable to compute dashboard."
