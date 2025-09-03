from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import urlparse

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://astranetix_user:secure_password@localhost:5432/astranetix_bms')

# Parse the database URL to get components
parsed_url = urlparse(DATABASE_URL)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv('DEBUG', 'false').lower() == 'true'
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with tables"""
    Base.metadata.create_all(bind=engine)

def close_db():
    """Close database connections"""
    engine.dispose()