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
    Initialize database tables and seed default data.
    Called on application startup.
    """
    # Import all models to register them with Base
    from models import engagement, phase, finding, scan, terminal, chat, report
    from models.engagement import Engagement, EngagementStatus
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("[DB] Database tables created successfully")
    
    # Ensure default engagement exists for Mentor Mode/Global Terminal
    db = SessionLocal()
    try:
        default_engagement = db.query(Engagement).filter(Engagement.id == "default").first()
        if not default_engagement:
            print("[DB] Creating default engagement for Mentor Mode...")
            new_engagement = Engagement(
                id="default",
                name="General Assistant",
                target="Internal",
                scope="General guidance and tool testing",
                status=EngagementStatus.ACTIVE.value
            )
            db.add(new_engagement)
            db.commit()
            print("[DB] Default engagement created successfully")
    except Exception as e:
        print(f"[DB] Error seeding default data: {str(e)}")
        db.rollback()
    finally:
        db.close()
