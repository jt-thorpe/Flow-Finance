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


class DummyPaginate:
    """Simulates Flask-SQLAlchemy's paginate object for testing."""
    def __init__(self, items, has_next):
        self.items = items
        self.has_next = has_next


class DummyTransaction:
    """Simulates a transaction object for testing."""
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {"id": self.id}


@pytest.fixture
def app():
    """Create a Flask test application with the transactions blueprint registered."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(transactions_blueprint)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


def test_get_transactions_cache_miss_db_hit_success(app, client, monkeypatch):
    """Test successful retrieval of transactions when cache misses but DB has data."""
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
        assert data["success"] is True
        assert data["data"]["transactions"] == [{"id": 1}, {"id": 2}]
        assert data["data"]["has_more"] is False


def test_get_transactions_cache_hit_success(app, client, monkeypatch):
    """Test successful retrieval of transactions from cache."""
    with app.app_context():
        g.user_id = "test_userid"
        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["transactions"] == [{"id": 1}, {"id": 2}]
        assert data["data"]["has_more"] is False


def test_get_transactions_cache_hit_pagination_fail(app, client, monkeypatch):
    """Test handling of pagination failure when data is retrieved from cache."""
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
        assert data["success"] is False
        assert data["message"] == "Unable to load transactions."


def test_get_transactions_cache_miss_db_hit_pagination_fail(app, client, monkeypatch):
    """Test handling of pagination failure when data is retrieved from database."""
    with app.app_context():
        g.user_id = "test_userid"
        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)
        sim_get_all_transactions_success(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )
        sim_pagination_fail(monkeypatch, prefix=FUNC_PREFIX)

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 500

        data = response.get_json()
        assert data["success"] is False
        assert data["message"] == "Unable to load transactions."


def test_get_transactions_cache_miss_db_miss_pagination_empty(app, client, monkeypatch):
    """Test handling of empty transaction list from both cache and database."""
    with app.app_context():
        g.user_id = "test_userid"

        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)
        sim_get_all_transactions_empty(monkeypatch, prefix=FUNC_PREFIX)
        sim_pagination_empty(monkeypatch, prefix=FUNC_PREFIX)

        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data["success"] is True
        assert data["data"] is None


def test_get_transactions_negative_page(app, client, monkeypatch):
    """Test handling of negative page parameter."""
    with app.app_context():
        g.user_id = "test_userid"
        sim_get_cache_field_hit(monkeypatch, prefix=FUNC_PREFIX, data=DummyTransactionsData().to_dict())
        
        response = client.get("/api/transactions/get-by?page=-1&limit=20")
        assert response.status_code == 400
        assert response.get_json()["success"] is False


def test_get_transactions_no_transactions(app, client, monkeypatch):
    """Test handling of user with no transactions."""
    with app.app_context():
        g.user_id = "test_userid"
        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)
        sim_get_all_transactions_empty(monkeypatch, prefix=FUNC_PREFIX)
        
        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200
        assert response.get_json()["success"] is True
        assert response.get_json()["data"] is None


def test_get_transactions_pagination_boundaries(app, client, monkeypatch):
    """Test pagination with various page sizes and boundaries."""
    with app.app_context():
        g.user_id = "test_userid"
        transactions = [{"id": i} for i in range(25)]
        sim_get_cache_field_hit(monkeypatch, prefix=FUNC_PREFIX, data=transactions)
        
        # Test first page
        response = client.get("/api/transactions/get-by?page=1&limit=10")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]["transactions"]) == 10
        assert data["data"]["has_more"] is True
        
        # Test middle page
        response = client.get("/api/transactions/get-by?page=2&limit=10")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]["transactions"]) == 10
        assert data["data"]["has_more"] is True
        
        # Test last page
        response = client.get("/api/transactions/get-by?page=3&limit=10")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]["transactions"]) == 5
        assert data["data"]["has_more"] is False


def test_get_transactions_pagination_error(app, client, monkeypatch):
    """Test handling of pagination errors."""
    with app.app_context():
        g.user_id = "test_userid"
        sim_get_cache_field_hit(monkeypatch, prefix=FUNC_PREFIX, data=DummyTransactionsData().to_dict())
        sim_pagination_fail(monkeypatch, prefix=FUNC_PREFIX)
        
        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 500
        assert response.get_json()["success"] is False
        assert response.get_json()["message"] == "Unable to load transactions."
