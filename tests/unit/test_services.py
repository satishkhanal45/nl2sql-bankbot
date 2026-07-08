# tests/unit/test_services.py
import pytest
from app.services.query_service import understand_query, extract_json_from_response
from app.services.search_service import format_value
from app.db.database import SessionLocal
from app.services.search_service import search_from_query_result
from app.services.query_service import understand_query


# ── Query Service Tests ──────────────────────────────────────

def test_extract_json_clean():
    """Verify clean JSON is parsed correctly."""
    response = '{"entity": "bank", "fact": "home_loan", "attribute": "interest_rate"}'
    result = extract_json_from_response(response)
    assert result["entity"] == "bank"
    assert result["fact"] == "home_loan"
    assert result["attribute"] == "interest_rate"


def test_extract_json_with_markdown():
    """Verify JSON wrapped in markdown is parsed correctly."""
    response = '```json\n{"entity": "bank", "fact": "home_loan", "attribute": "interest_rate"}\n```'
    result = extract_json_from_response(response)
    assert result is not None
    assert result["fact"] == "home_loan"


def test_extract_json_invalid():
    """Verify invalid JSON returns None."""
    result = extract_json_from_response("this is not json at all")
    assert result is None


def test_understand_query_home_loan():
    """Verify home loan question is understood correctly."""
    result = understand_query("What is the home loan interest rate?")
    assert result["success"] is True
    assert result["fact"] == "home_loan"
    assert result["attribute"] == "interest_rate"


def test_understand_query_out_of_scope():
    """Verify out of scope questions fail gracefully."""
    result = understand_query("What is the weather today?")
    assert result["success"] is False


# ── Search Service Tests ─────────────────────────────────────

def test_format_value_interest_rate():
    """Verify interest rate is formatted with %."""
    assert format_value("8.5", "numeric", "interest_rate") == "8.5%"


def test_format_value_loan_amount():
    """Verify loan amount is formatted with NPR and commas."""
    assert format_value("5000000", "numeric", "minimum_loan_amount") == "NPR 5,000,000"


def test_format_value_tenure():
    """Verify tenure is formatted with years."""
    assert format_value("25", "numeric", "minimum_tenure") == "25 years"





def test_format_value_string():
    """Verify string values are returned as-is."""
    assert format_value("Baneshwor", "string", "address") == "Baneshwor"


def test_format_value_processing_fee():
    """Verify processing fee is formatted with %."""
    assert format_value("1.0", "numeric", "processing_fee") == "1.0%"


def test_search_from_query_result_success():
    """Verify full search pipeline returns correct data."""
    db = SessionLocal()
    try:
        query_result = {
            "success": True,
            "entity": "bank",
            "fact": "home_loan",
            "attribute": "interest_rate",
            "original_question": "What is the home loan interest rate?",
        }
        result = search_from_query_result(db, query_result)
        assert result["success"] is True
        assert result["found"] is True
        assert result["data"]["value"] == "8.5"
        assert result["data"]["formatted_value"] == "8.5%"
    finally:
        db.close()


def test_search_from_query_result_failed_query():
    """Verify failed query understanding is handled gracefully."""
    db = SessionLocal()
    try:
        query_result = {
            "success": False,
            "entity": "bank",
            "fact": None,
            "attribute": None,
            "original_question": "What is the weather?",
            "error": "Question not understood",
        }
        result = search_from_query_result(db, query_result)
        assert result["success"] is False
        assert result["found"] is False
    finally:
        db.close()