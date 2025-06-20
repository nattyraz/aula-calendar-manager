"""
Configuration base de donn?es
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.database_url, 
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_database():
    """G?n?rateur de session de base de donn?es"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()