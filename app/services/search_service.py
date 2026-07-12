# app/services/search_service.py
from sqlalchemy.orm import Session
from app.db.repositories import entity_repository
from typing import Optional


def format_value(value: str, type: str, attribute: str) -> str:
    """
    Formats a raw database value into a human-readable string.
    """
    if type == "numeric":
        if attribute in ("interest_rate", "processing_fee", "cashback"):
            return f"{value}%"
        elif attribute in (
            "minimum_loan_amount", "maximum_loan_amount",
            "minimum_deposit", "maximum_deposit",
            "cash_withdrawal_limit", "transaction_limit",
            "annual_fee", "joining_fee", "replacement_fee",
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

    Handles five query types:
    - specific:        exact LTREE path match
    - broad_instance:  all attributes of one instance
    - broad_category:  everything under a category
    - attribute_only:  all rows matching an attribute label
    - unknown:         query understanding failed
    """
    if not query_result.get("success"):
        return {
            "success":    False,
            "found":      False,
            "query_type": "unknown",
            "data":       None,
            "query":      query_result,
            "error":      query_result.get("error", "Query understanding failed"),
        }

    entity     = query_result["entity"]
    fact       = query_result.get("fact")
    instance   = query_result.get("instance")
    attribute  = query_result.get("attribute")
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
            "success":    True,
            "found":      False,
            "query_type": query_type,
            "data":       None,
            "query":      query_result,
            "error": (
                f"No data found for {entity}"
                + (f".{fact}"      if fact      else "")
                + (f".{instance}"  if instance  else "")
                + (f".{attribute}" if attribute else ".*")
            ),
        }

    # For specific queries add formatted value
    if db_result["query_type"] == "specific":
        data = db_result["data"]
        data["entity"]          = entity
        data["fact"]            = fact
        data["instance"]        = instance
        data["attribute"]       = attribute
        data["formatted_value"] = format_value(
            data["value"],
            data["type"],
            attribute,
        )

    # For attribute_only queries add formatted value to each row
    if db_result["query_type"] == "attribute_only":
        for row in db_result["data"]:
            row["formatted_value"] = format_value(
                row["value"],
                row["type"],
                row["attribute"],
            )

    return {
        "success":    True,
        "found":      True,
        "query_type": db_result["query_type"],
        "data":       db_result["data"],
        "query":      query_result,
        "error":      None,
    }