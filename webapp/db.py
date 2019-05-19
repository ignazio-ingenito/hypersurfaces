import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

if 'POSTGRES_USER' in os.environ:
    user = os.environ['POSTGRES_USER']
    pwd = os.environ['POSTGRES_PASSWORD']
    db = os.environ['POSTGRES_DB']
    host = 'db'  # docker-compose creates a hostname alias with the service name
else:
    user = 'postgres'
    pwd = 'postgres'
    db = 'flaskapp_db'
    host = '127.0.0.1'

port = '5432'  # default postgres port

engine = create_engine(f'postgres://{user}:{pwd}@{host}:{port}/{db}')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
# Base.query = db_session.query_property()