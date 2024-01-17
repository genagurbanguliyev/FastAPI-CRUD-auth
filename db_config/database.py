from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config


DB_HOST = config("DB_HOST")
HOST_NAME = config("HOST_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST_PORT = config("DB_HOST_PORT")
DB_NAME = config("DB_NAME")


# use SQLite database
# SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

SQLALCHEMY_DATABASE_URL = f"{DB_HOST}://{DB_USER}:{DB_PASSWORD}@{HOST_NAME}:{DB_HOST_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()