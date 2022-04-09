from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from Parameters import Parameters

def get_database_uri():
    parameter = Parameters()
    return parameter.database

SQLALCHEMY_DATABASE_URI = get_database_uri()

engine = create_engine(SQLALCHEMY_DATABASE_URI)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
#session = Session()

Base = declarative_base()

def get_session():
    return Session()

def remove_session():
    Session.remove()

