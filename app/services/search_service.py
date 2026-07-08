# app/services/search_service.py
from sqlalchemy.orm import Session
from app.db.repositories import entity_repository
from typing import Optional


def format_value(value: str, type: str, attribute: str) -> str:
    """
    Formats a raw database value into a human-readable string.

    Rules:
    - interest_rate, processing_fee, cashback → append %
    - loan amounts, deposits, limits, fees    → prepend NPR with commas
    - tenure                                  → append years
    - everything else                         → return as-is

    Examples:
        format_value("8.5",     "numeric", "interest_rate")      → "8.5%"
        format_value("5000000", "numeric", "minimum_loan_amount") → "NPR 5,000,000"
        format_value("25",      "numeric", "maximum_tenure")      → "25 years"
        format_value("Baneshwor", "string", "address")            → "Baneshwor"
    """
    if type == "numeric":
        if attribute in ("interest_rate", "processing_fee", "cashback"):
            return f"{value}%"
        elif attribute in (
            "minimum_loan_amount",
            "maximum_loan_amount",
            "minimum_deposit",
            "maximum_deposit",
            "cash_withdrawal_limit",
            "transaction_limit",
            "annual_fee",
            "joining_fee",
            "replacement_fee",
        ):
            try:
                return f"NPR {int(float(value)):,}"
            except ValueError:
                return value
        elif attribute in ("minimum_tenure", "maximum_tenure"):
            return f"{value} years"
    return value


def search_from_query_result(db: Session, query_result: dict) -> dict:
    """
    Takes the output of understand_query() and searches the database.

    Three query types:
    - specific:        exact LTREE path match
    - broad_instance:  all attributes of one instance
    - broad_category:  everything under a category
    """
    if not query_result.get("success"):
        return {
            "success": False,
            "found": False,
            "query_type": "unknown",
            "data": None,
            "query": query_result,
            "error": query_result.get("error", "Query understanding failed"),
        }

    entity    = query_result["entity"]
    fact      = query_result["fact"]
    instance  = query_result.get("instance")
    attribute = query_result.get("attribute")
    query_type = query_result.get("query_type", "specific")

    db_result = entity_repository.search_by_query_type(
        db=db,
        entity_name=entity,
        fact=fact,
        instance=instance,
        attribute=attribute,
    )

    if not db_result["found"]:
        return {
            "success": True,
            "found": False,
            "query_type": query_type,
            "data": None,
            "query": query_result,
            "error": (
                f"No data found for {entity}.{fact}"
                + (f".{instance}" if instance else "")
                + (f".{attribute}" if attribute else ".*")
            ),
        }

    # For specific queries, add formatted value
    if db_result["query_type"] == "specific":
        data = db_result["data"]
        data["entity"]   = entity
        data["fact"]     = fact
        data["instance"] = instance
        data["attribute"] = attribute
        data["formatted_value"] = format_value(
            data["value"],
            data["type"],
            attribute,
        )

    return {
        "success": True,
        "found": True,
        "query_type": db_result["query_type"],
        "data": db_result["data"],
        "query": query_result,
        "error": None,
    }