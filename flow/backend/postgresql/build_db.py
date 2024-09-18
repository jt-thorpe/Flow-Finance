from sqlalchemy import create_engine

from flow.backend.postgresql.connect import get_db_uri
from flow.backend.postgresql.tables import Base


def build_db_tables() -> None:
    """Build the tables for the DB."""
    engine = create_engine(url=get_db_uri(), echo=True)

    # Our MetaData obj is part of our Base class, generated with DeclaritiveBase.
    # As our tables, such as 'User', for example are subclasses of our Base,
    # they are automaticlaly associated with the `Base.metadata` obj.
    Base.metadata.create_all(engine)
