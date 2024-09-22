"""For connecting and experimenting with the PostgreSQL DB initially.

You need to set the FLOW_DB_URI environment varible to connect to the DB.
This is to keep the credentials out of version control.

ENVIRONMENT_VARIABLES:
    - FLOW_DB_URI: the URI from the postgresql hosting service
"""

import os

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(url=os.environ["FLOW_DB_URI"], echo=True)
Session = sessionmaker(bind=engine)


def get_session():
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
