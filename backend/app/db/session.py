"""Database Session and Engine Configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database URL for SQLite
# Use absolute path for database file in database/ folder
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "quick_tym.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create database engine with SQLite-specific options
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Get database session
def get_db():
    """Dependency for FastAPI routes to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
