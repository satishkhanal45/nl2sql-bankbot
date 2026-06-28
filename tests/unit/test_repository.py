# tests/unit/test_repository.py
import pytest
from app.db.database import SessionLocal
from app.db.repositories import entity_repository


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


def test_get_entity_by_name_and_fact(db):
    """Verify we can fetch an entity by name and fact."""
    entity = entity_repository.get_entity_by_name_and_fact(
        db, "bank", "home_loan"
    )
    assert entity is not None
    assert entity.entity_name == "bank"
    assert entity.fact == "home_loan"


def test_get_entity_returns_none_for_unknown(db):
    """Verify None is returned for unknown entities."""
    entity = entity_repository.get_entity_by_name_and_fact(
        db, "unknown", "unknown"
    )
    assert entity is None


def test_get_attribute_by_label(db):
    """Verify we can fetch an attribute by label."""
    attribute = entity_repository.get_attribute_by_label(db, "interest_rate")
    assert attribute is not None
    assert attribute.label == "interest_rate"


def test_get_attribute_returns_none_for_unknown(db):
    """Verify None is returned for unknown attributes."""
    attribute = entity_repository.get_attribute_by_label(db, "unknown_attr")
    assert attribute is None


def test_get_value_by_entity_fact_attribute(db):
    """Verify the main query function returns correct values."""
    result = entity_repository.get_value_by_entity_fact_attribute(
        db, "bank", "home_loan", "interest_rate"
    )
    assert result is not None
    assert result["value"] == "8.5"
    assert result["type"] == "numeric"
    assert result["path_name"] == "bank.home_loan.interest_rate"


def test_get_value_returns_none_for_unknown(db):
    """Verify None is returned when no match exists."""
    result = entity_repository.get_value_by_entity_fact_attribute(
        db, "bank", "unknown_fact", "unknown_attr"
    )
    assert result is None


def test_get_all_facts_for_entity(db):
    """Verify all facts for bank are returned."""
    facts = entity_repository.get_all_facts_for_entity(db, "bank")
    assert len(facts) > 0
    fact_names = [f["fact"] for f in facts]
    assert "home_loan" in fact_names
    assert "saving_account" in fact_names


def test_get_values_by_ltree_path(db):
    """Verify LTREE path queries work correctly."""
    results = entity_repository.get_values_by_ltree_path(
        db, "bank.home_loan"
    )
    assert len(results) > 0
    path_names = [r["path_name"] for r in results]
    assert "bank.home_loan.interest_rate" in path_names
    assert "bank.home_loan.loan_amount" in path_names