# app/services/search_service.py
from sqlalchemy.orm import Session
from app.db.repositories import entity_repository
from typing import Optional


def search_database(
    db: Session,
    entity: str,
    fact: str,
    attribute: str,
) -> Optional[dict]:
    """
    Searches the database using entity, fact, and attribute.

    Args:
        db: SQLAlchemy session
        entity: The entity name (e.g. "bank")
        fact: The fact name (e.g. "home_loan")
        attribute: The attribute label (e.g. "interest_rate")

    Returns:
        {
            "value": "8.5",
            "type": "numeric",
            "path_name": "bank.home_loan.interest_rate",
            "entity": "bank",
            "fact": "home_loan",
            "attribute": "interest_rate",
            "formatted_value": "8.5%",
        }
        Or None if not found.
    """
    result = entity_repository.get_value_by_entity_fact_attribute(
        db=db,
        entity_name=entity,
        fact=fact,
        attribute=attribute,
    )

    if result is None:
        return None

    return {
        "value": result["value"],
        "type": result["type"],
        "path_name": result["path_name"],
        "entity": entity,
        "fact": fact,
        "attribute": attribute,
        "formatted_value": format_value(result["value"], result["type"], attribute),
    }


def format_value(value: str, type: str, attribute: str) -> str:
    """
    Formats a raw database value into a human-readable string.

    Rules:
    - interest_rate → append %
    - processing_fee → append %
    - loan_amount / minimum_balance / maximum_balance → append NPR and add commas
    - tenure → append years
    - Everything else → return as-is

    Examples:
        format_value("8.5", "numeric", "interest_rate") → "8.5%"
        format_value("5000000", "numeric", "loan_amount") → "NPR 5,000,000"
        format_value("20", "numeric", "tenure") → "20 years"
        format_value("Baneshwor", "string", "address") → "Baneshwor"
    """
    if type == "numeric":
        if attribute in ("interest_rate", "processing_fee"):
            return f"{value}%"
        elif attribute in ("loan_amount", "minimum_balance", "maximum_balance"):
            try:
                return f"NPR {int(float(value)):,}"
            except ValueError:
                return value
        elif attribute == "tenure":
            return f"{value} years"

    return value


def search_from_query_result(db: Session, query_result: dict) -> dict:
    """
    Takes the output of understand_query() and searches the database.

    This is the main bridge between Phase 10 (query understanding)
    and Phase 11 (database search).

    Args:
        db: SQLAlchemy session
        query_result: Output from understand_query()

    Returns:
        {
            "success": True/False,
            "found": True/False,
            "data": {...} or None,
            "query": {...},
            "error": "..." or None,
        }
    """
    # If query understanding failed, pass the error through
    if not query_result.get("success"):
        return {
            "success": False,
            "found": False,
            "data": None,
            "query": query_result,
            "error": query_result.get("error", "Query understanding failed"),
        }

    entity = query_result["entity"]
    fact = query_result["fact"]
    attribute = query_result["attribute"]

    db_result = search_database(
        db=db,
        entity=entity,
        fact=fact,
        attribute=attribute,
    )

    if db_result is None:
        return {
            "success": True,
            "found": False,
            "data": None,
            "query": query_result,
            "error": f"No data found for {entity} → {fact} → {attribute}",
        }

    return {
        "success": True,
        "found": True,
        "data": db_result,
        "query": query_result,
        "error": None,
    }