# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db
from app.core.config import get_settings

settings = get_settings()


@pytest.fixture(scope="session")
def db_engine():
    """
    Creates a database engine for the test session.
    Uses the same database as development since we're testing
    against real data.
    """
    engine = create_engine(settings.database_url)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Creates a fresh database session for each test.
    Rolls back after each test so tests don't affect each other.
    """
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Creates a FastAPI test client with a real database session.
    Overrides the get_db dependency to use our test session.
    """
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()