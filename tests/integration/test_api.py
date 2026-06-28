# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify root endpoint returns app info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app" in data
    assert "docs" in data


def test_health_endpoint():
    """Verify health endpoint returns ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"


def test_chat_endpoint_valid_question():
    """Verify chat endpoint handles a valid bank question."""
    response = client.post(
        "/chat",
        json={"question": "What is the home loan interest rate?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["query"]["fact"] == "home_loan"
    assert data["query"]["attribute"] == "interest_rate"
    assert data["data"]["value"] == "8.5"
    assert "8.5" in data["answer"]


def test_chat_endpoint_vehicle_loan():
    """Verify chat endpoint handles vehicle loan question."""
    response = client.post(
        "/chat",
        json={"question": "What is the vehicle loan interest rate?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["value"] == "11.0"


def test_chat_endpoint_out_of_scope():
    """Verify chat endpoint handles out of scope questions."""
    response = client.post(
        "/chat",
        json={"question": "What is the weather today?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["data"] is None


def test_chat_endpoint_empty_question():
    """Verify chat endpoint rejects empty questions."""
    response = client.post(
        "/chat",
        json={"question": ""},
    )
    assert response.status_code == 422


def test_chat_endpoint_missing_question():
    """Verify chat endpoint rejects missing question field."""
    response = client.post(
        "/chat",
        json={},
    )
    assert response.status_code == 422


def test_chat_endpoint_saving_account():
    """Verify chat endpoint handles saving account question."""
    response = client.post(
        "/chat",
        json={"question": "What is the minimum balance for a saving account?"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["value"] == "1000"