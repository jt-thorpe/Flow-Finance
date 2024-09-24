"""For connecting and experimenting with the PostgreSQL DB initially.

You need to set the FLOW_DB_URI environment varible to connect to the DB.
This is to keep the credentials out of version control.

ENVIRONMENT_VARIABLES:
    - FLOW_DB_URI: the URI from the postgresql hosting service
"""

import os

import psycopg2
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from flow.backend.postgresql.models import Transaction, User

engine = create_engine(url=os.environ["FLOW_DB_URI"], echo=True)
Session = sessionmaker(bind=engine)


def get_session():
    """Get the Session object."""
    return Session()


def get_db_uri() -> str:
    """Get the databse URI from the environment varaible.

    Raises:
        ValueError, if the FLOW_DB_URI environment variable is not set.

    Returns:
        str, the FLOW_DB_URI environment variable.
    """
    service_uri = os.environ["FLOW_DB_URI"]
    if not service_uri:
        raise ValueError("FLOW_DB_URI: environment variable is not set.")
    else:
        return service_uri


def get_db_connection():
    service_uri = get_db_uri()

    # Establish a connection to the DB
    return psycopg2.connect(service_uri)


def get_user_transactions(user_id: str) -> list[Transaction]:  # Hint might be wrong
    """Get all transactions for a User.

    Args:
        user_id, str: the UUID of the user taken from the JWT token.

    Returns:
        list[Transaction]: a list of Transaction objects.
    """
    transactions = get_session().execute(
        select(Transaction.id,
               Transaction.date,
               Transaction.description,
               Transaction.category,
               Transaction.amount).where(User.id == user_id)
    ).all()

    return transactions
