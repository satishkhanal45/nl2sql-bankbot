# app/db/database.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.core.config import get_settings

settings = get_settings()

# The engine is the core connection to PostgreSQL
# pool_pre_ping=True checks the connection is alive before using it
# pool_size=5 keeps 5 connections open and ready
# max_overflow=10 allows up to 10 extra connections under heavy load
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=settings.debug,  # logs all SQL queries in development
)

# SessionLocal is a factory that creates new Session objects
# autocommit=False means we control when to commit transactions
# autoflush=False means changes aren't sent to DB until we flush/commit
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    Usage in FastAPI routes:
        @app.get("/example")
        def example(db: Session = Depends(get_db)):
            ...

    The 'yield' makes this a context manager:
    - Opens a session before the request
    - Closes it after the request (even if an error occurs)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """
    Tests if the database is reachable.
    Used in the health check endpoint.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False