# agentops-server/app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.config import POSTGRES_URL

engine = create_engine(
    POSTGRES_URL,
    pool_pre_ping=True,
    # optional:
    # pool_size=10,
    # max_overflow=20,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """
    Dependency that yields a SQLAlchemy DB session.
    Closes it after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
