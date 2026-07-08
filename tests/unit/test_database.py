# tests/unit/test_database.py
import pytest
from app.db.database import check_db_connection, SessionLocal
from app.db.models.entity import Entity, Attribute, EntityValue


def test_database_connection():
    """Verify we can connect to PostgreSQL."""
    assert check_db_connection() is True


def test_entity_table_has_data():
    entities = db.query(Entity).all()
    assert len(entities) == 7  # 7 categories now
    facts = [e.fact for e in entities]
    assert "loan" in facts
    assert "branch" in facts
    assert "account" in facts

def test_attribute_table_has_data():
    attributes = db.query(Attribute).all()
    assert len(attributes) == 50

def test_entity_value_table_has_data():
    """Verify the entity_value table has our seed data."""
    db = SessionLocal()
    try:
        values = db.query(EntityValue).all()
        assert len(values) > 0
    finally:
        db.close()


def test_entity_relationships():
    """Verify SQLAlchemy relationships work correctly."""
    db = SessionLocal()
    try:
        entity = db.query(Entity).filter_by(fact="home_loan").first()
        assert entity is not None
        assert entity.entity_name == "bank"
        assert len(entity.values) > 0
    finally:
        db.close()