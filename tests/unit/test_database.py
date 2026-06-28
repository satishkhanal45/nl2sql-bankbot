# tests/unit/test_database.py
import pytest
from app.db.database import check_db_connection, SessionLocal
from app.db.models.entity import Entity, Attribute, EntityValue


def test_database_connection():
    """Verify we can connect to PostgreSQL."""
    assert check_db_connection() is True


def test_entity_table_has_data():
    """Verify the entity table has our seed data."""
    db = SessionLocal()
    try:
        entities = db.query(Entity).all()
        assert len(entities) == 8
        entity_facts = [e.fact for e in entities]
        assert "home_loan" in entity_facts
        assert "saving_account" in entity_facts
        assert "vehicle_loan" in entity_facts
    finally:
        db.close()


def test_attribute_table_has_data():
    """Verify the attribute table has our seed data."""
    db = SessionLocal()
    try:
        attributes = db.query(Attribute).all()
        assert len(attributes) == 13
        labels = [a.label for a in attributes]
        assert "interest_rate" in labels
        assert "loan_amount" in labels
        assert "tenure" in labels
    finally:
        db.close()


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