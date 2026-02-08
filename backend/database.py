"""
HackMate v2.0 - Database Configuration
SQLAlchemy setup for SQLite database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# Create SQLite engine
# check_same_thread is False for SQLite to allow multiple threads
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    Called on application startup.
    """
    # Import all models to register them with Base
    from models import engagement, phase, finding, scan, terminal, chat, report
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("[DB] Database tables created successfully")
