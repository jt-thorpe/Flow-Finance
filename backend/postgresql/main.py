"""For connecting and experimenting with the PostgreSQL DB initially.

You need to set the FLOW_DB_URI environment varible to connect to the DB.
This is to keep the credentials out of version control.

ENVIRONMENT_VARIABLES:
    - FLOW_DB_URI: the URI from the postgresql hosting service
"""


import os

import psycopg2


def main():
    service_uri = os.environ["FLOW_DB_URI"]
    if not service_uri:
        raise ValueError("FLOW_DB_URI: environment variable is not set.")

    conn = psycopg2.connect(service_uri)

    query_sql = 'SELECT VERSION()'

    cur = conn.cursor()
    cur.execute(query_sql)

    version = cur.fetchone()[0]
    print(version)


if __name__ == "__main__":
    main()
