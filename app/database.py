import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.settings.base import settings


SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (settings.PG_USER, settings.PG_PASSWORD, settings.PG_HOST, settings.PG_DATABASE)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
