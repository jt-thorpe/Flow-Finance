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


def test_list_transactions_cache_miss_db_success(app, client, monkeypatch):
    """Test successful retrieval of transactions when cache misses but DB has data."""
    with app.app_context():
        g.user_id = "test_userid"
        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)
        sim_get_all_transactions_success(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        response = client.get("/api/transactions/list?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Transactions retrieved successfully",
            "transactions": [{"id": 1}, {"id": 2}],
            "has_more": False
        }


def test_list_transactions_cache_hit_success(app, client, monkeypatch):
    """Test successful retrieval of transactions from cache."""
    with app.app_context():
        g.user_id = "test_userid"
        dummy_transactions = DummyTransactionsData().to_dict()

        sim_get_cache_field_hit(
            monkeypatch, prefix=FUNC_PREFIX, data=dummy_transactions
        )

        response = client.get("/api/transactions/list?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Transactions retrieved successfully",
            "transactions": [{"id": 1}, {"id": 2}],
            "has_more": False
        }


def test_list_transactions_pagination_error(app, client, monkeypatch):
    """Test handling of pagination errors."""
    with app.app_context():
        g.user_id = "test_userid"
        sim_get_cache_field_hit(monkeypatch, prefix=FUNC_PREFIX, data=DummyTransactionsData().to_dict())
        sim_pagination_fail(monkeypatch, prefix=FUNC_PREFIX)
        
        response = client.get("/api/transactions/list?page=1&limit=20")
        assert response.status_code == 500
        data = response.get_json()
        assert data == {
            "success": False,
            "message": "Error paginating transactions"
        }


def test_list_transactions_no_transactions(app, client, monkeypatch):
    """Test handling of user with no transactions."""
    with app.app_context():
        g.user_id = "test_userid"
        sim_get_cache_field_miss(monkeypatch, prefix=FUNC_PREFIX)
        sim_get_all_transactions_empty(monkeypatch, prefix=FUNC_PREFIX)
        sim_pagination_empty(monkeypatch, prefix=FUNC_PREFIX)
        
        response = client.get("/api/transactions/list?page=1&limit=20")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "success": True,
            "message": "No transactions found",
            "transactions": [],
            "has_more": False
        }


def test_list_transactions_invalid_pagination(app, client, monkeypatch):
    """Test handling of invalid pagination parameters."""
    with app.app_context():
        g.user_id = "test_userid"
        sim_get_cache_field_hit(monkeypatch, prefix=FUNC_PREFIX, data=DummyTransactionsData().to_dict())
        
        # Test negative page
        response = client.get("/api/transactions/list?page=-1&limit=20")
        assert response.status_code == 400
        data = response.get_json()
        assert data == {
            "success": False,
            "message": "Invalid page or limit parameters"
        }
        
        # Test negative limit
        response = client.get("/api/transactions/list?page=1&limit=-1")
        assert response.status_code == 400
        data = response.get_json()
        assert data == {
            "success": False,
            "message": "Invalid page or limit parameters"
        }


def test_list_transactions_pagination_boundaries(app, client, monkeypatch):
    """Test pagination with various page sizes and boundaries."""
    with app.app_context():
        g.user_id = "test_userid"
        transactions = [{"id": i} for i in range(25)]
        sim_get_cache_field_hit(monkeypatch, prefix=FUNC_PREFIX, data=transactions)
        
        # Test first page
        response = client.get("/api/transactions/list?page=1&limit=10")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Transactions retrieved successfully",
            "transactions": [{"id": i} for i in range(10)],
            "has_more": True
        }
        
        # Test middle page
        response = client.get("/api/transactions/list?page=2&limit=10")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Transactions retrieved successfully",
            "transactions": [{"id": i} for i in range(10, 20)],
            "has_more": True
        }
        
        # Test last page
        response = client.get("/api/transactions/list?page=3&limit=10")
        assert response.status_code == 200
        data = response.get_json()
        assert data == {
            "success": True,
            "message": "Transactions retrieved successfully",
            "transactions": [{"id": i} for i in range(20, 25)],
            "has_more": False
        }


def test_list_transactions_unexpected_error(app, client, monkeypatch):
    """Test handling of unexpected errors in the list_transactions endpoint."""
    with app.app_context():
        g.user_id = "test_userid"
        
        # Simulate an unexpected error in cache service
        def raise_error(user_id, field):
            raise Exception("Unexpected error")
            
        monkeypatch.setattr(
            "backend.routes.transactions_routes.get_user_cache_field",
            raise_error
        )

        response = client.get("/api/transactions/list?page=1&limit=20")
        assert response.status_code == 500
        data = response.get_json()
        assert data == {
            "success": False,
            "message": "Internal server error while retrieving transactions"
        }
