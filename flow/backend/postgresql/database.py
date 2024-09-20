import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # Base class for DB models
engine = create_engine(url=os.environ["FLOW_DB_URI"], echo=True)
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
