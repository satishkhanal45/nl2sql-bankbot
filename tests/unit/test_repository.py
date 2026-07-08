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
    """Verify search_by_query_type returns correct value for specific query."""
    result = entity_repository.search_by_query_type(
        db, "bank", "home_loan", "interest_rate"
    )
    assert result["found"] is True
    assert result["query_type"] == "specific"
    assert result["data"]["value"] == "8.5"
    assert result["data"]["path_name"] == "bank.home_loan.interest_rate"


def test_get_value_returns_none_for_unknown(db):
    """Verify search_by_query_type returns not found for unknown path."""
    result = entity_repository.search_by_query_type(
        db, "bank", "unknown_fact", "unknown_attr"
    )
    assert result["found"] is False


def test_get_all_facts_for_entity(db):
    """Verify all facts for bank are returned."""
    facts = entity_repository.get_all_facts_for_entity(db, "bank")
    assert len(facts) > 0
    fact_names = [f["fact"] for f in facts]
    assert "home_loan" in fact_names
    assert "saving_account" in fact_names


def test_search_by_query_type_specific(db):
    """Verify specific query returns single value via exact LTREE match."""
    result = entity_repository.search_by_query_type(
        db, "bank", "home_loan", "interest_rate"
    )
    assert result["query_type"] == "specific"
    assert result["found"] is True
    assert result["data"]["value"] == "8.5"
    assert result["data"]["path_name"] == "bank.home_loan.interest_rate"


def test_search_by_query_type_broad(db):
    """Verify broad query returns all values under a path prefix."""
    result = entity_repository.search_by_query_type(
        db, "bank", "home_loan", None
    )
    assert result["query_type"] == "broad"
    assert result["found"] is True
    assert len(result["data"]) > 0
    path_names = [r["path_name"] for r in result["data"]]
    assert "bank.home_loan.interest_rate" in path_names
    assert "bank.home_loan.loan_type" in path_names


def test_search_by_query_type_not_found(db):
    """Verify not found returned for unknown path."""
    result = entity_repository.search_by_query_type(
        db, "bank", "unknown_fact", "unknown_attr"
    )
    assert result["found"] is False


def test_search_by_query_type_broad_not_found(db):
    """Verify not found returned for unknown broad path."""
    result = entity_repository.search_by_query_type(
        db, "bank", "unknown_fact", None
    )
    assert result["found"] is False
    assert result["data"] == []