from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import POSTGRES_URL

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
