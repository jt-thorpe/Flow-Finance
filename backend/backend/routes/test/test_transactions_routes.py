import backend.services.auth_services
import pytest
from flask import Flask, g

# Bypass the login_required decorator
backend.services.auth_services.login_required = lambda f: f

from backend.models.transaction_models import Transaction
from backend.routes.transactions_routes import transactions_blueprint


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


def test_get_transactions_success(app, client, monkeypatch):
    """Test the case where transactions are returned."""
    with app.app_context():
        g.user_id = "test_userid"

        # Create dummy transactions and a dummy paginate object.
        dummy_transactions = [DummyTransaction(1), DummyTransaction(2)]
        dummy_paginate = DummyPaginate(dummy_transactions, has_next=False)

        # Patch the query chain in Transaction so that order_by().paginate() returns our dummy_paginate.
        class DummyQuery:
            def order_by(self, ordering):
                return self

            def paginate(self, page, per_page, error_out):
                return dummy_paginate

        monkeypatch.setattr(Transaction, "query", DummyQuery())

        # Send request with page and limit parameters.
        response = client.get("/api/transactions/get-by?page=1&limit=20")
        assert response.status_code == 200

        data = response.get_json()
        # Expected to return the list of transactions and has_more = False.
        assert "transactions" in data
        assert data["transactions"] == [{"id": 1}, {"id": 2}]
        assert data["has_more"] is False


def test_get_transactions_empty(app, client, monkeypatch):
    """Test the case where no transactions are found."""
    with app.app_context():
        g.user_id = "test_userid"

        dummy_paginate = DummyPaginate([], has_next=False)

        class DummyQuery:
            def order_by(self, ordering):
                return self

            def paginate(self, page, per_page, error_out):
                return dummy_paginate

        monkeypatch.setattr(Transaction, "query", DummyQuery())

        response = client.get("/api/transactions/get-by")
        assert response.status_code == 200

        data = response.get_json()
        assert data["transactions"] == []
        assert data["has_more"] is False
