from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Using SqlLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


# connect_args={"check_same_thread": False} is ONLY needed for SQLite.
# It allows multiple requests to talk to the DB at once.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of this class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# We will use this in the next file to create our tables.
Base = declarative_base()