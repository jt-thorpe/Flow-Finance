from typing import Final

import backend.services.auth_services
import pytest
from backend.routes.test.utils import (
    DummyTransactionsData,
    sim_get_all_transactions_empty,
    sim_get_all_transactions_success,
    sim_get_cache_field_hit,
    sim_get_cache_field_miss,
    sim_pagination_empty,
    sim_pagination_fail,
)
from flask import Flask, g

# Bypass the login_required decorator
backend.services.auth_services.login_required = lambda f: f

from backend.routes.transactions_routes import transactions_blueprint

FUNC_PREFIX: Final[str] = "backend.routes.transactions_routes"


# Dummy classes to simulate query pagination and transactions
class DummyPaginate:
    def __init__(self, items, has_next):
        self.items = items
        self.has_next = has_next


class DummyTransaction:
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {"id": self.id}


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(transactions_blueprint)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_transactions_cache_miss_db_hit_success(app, client, monkeypatch):
    """Test the case where we miss the cache but get_all_transactions and return."""
    with app.app_context():
        g.user_id = "test_userid"

        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)

        sim_get_all_transactions_success(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] == True
        assert data["data"]["transactions"] == [{"id": 1}, {"id": 2}]
        assert data["data"]["has_more"] is False


def test_get_transactions_cache_hit_success(app, client, monkeypatch):
    """Test the case where we hit the cache return the paginated results."""
    with app.app_context():
        g.user_id = "test_userid"

        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] == True
        assert data["data"]["transactions"] == [{"id": 1}, {"id": 2}]
        assert data["data"]["has_more"] is False


def test_get_transactions_cache_hit_pagination_fail(app, client, monkeypatch):
    """
    Test the case where we hit the cache but paginate_transactions fails.
    We simulate a cache hit and then patch paginate_transactions to raise an exception.
    Expecting a 500 error.
    """
    with app.app_context():
        g.user_id = "test_userid"

        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        sim_pagination_fail(monkeypatch, prefix=FUNC_PREFIX)

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 500

        data = response.get_json()
        assert data["success"] == False
        assert data["message"] == "Unable to load transactions."


def test_get_transactions_cache_miss_db_hit_pagination_fail(app, client, monkeypatch):
    """
    Test the case where we miss the cache, hit the DB, but then paginate_transactions fails.
    We simulate a cache miss and a successful DB hit (via get_all_transactions),
    then patch paginate_transactions to raise an exception.
    Expecting a 500 error.
    """
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)

        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_all_transactions_success(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        sim_pagination_fail(monkeypatch, prefix=FUNC_PREFIX)

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 500

        data = response.get_json()
        assert data["success"] == False
        assert data["message"] == "Unable to load transactions."


def test_get_transactions_cache_miss_db_miss_pagination_empty(app, client, monkeypatch):
    """
    Test the case where both the cache and the DB miss (i.e. no transactions found).
    In this scenario, get_all_transactions returns an empty list.
    Pagination of an empty list should succeed and return an empty result.
    """
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)

        sim_get_all_transactions_empty(monkeypatch, prefix=FUNC_PREFIX)

        sim_pagination_empty(monkeypatch, prefix=FUNC_PREFIX)

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] == True
        assert data["data"] == None
