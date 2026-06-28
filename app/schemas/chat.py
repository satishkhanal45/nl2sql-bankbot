# app/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """
    The request body for POST /chat.
    FastAPI automatically validates this — if 'question' is missing,
    it returns a 400 error before your code even runs.
    """
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The user's question in plain English",
        examples=["What is the home loan interest rate?"],
    )


class QueryInfo(BaseModel):
    """
    The structured JSON extracted from the question by the LLM.
    Included in the response for transparency/debugging.
    """
    entity: Optional[str] = None
    fact: Optional[str] = None
    attribute: Optional[str] = None


class DataInfo(BaseModel):
    """
    The raw data retrieved from the database.
    Included in the response for transparency/debugging.
    """
    value: Optional[str] = None
    type: Optional[str] = None
    path_name: Optional[str] = None
    formatted_value: Optional[str] = None


class ChatResponse(BaseModel):
    """
    The response body for POST /chat.
    """
    question: str = Field(description="The original question")
    answer: str = Field(description="The natural language answer")
    success: bool = Field(description="Whether the question was answered")
    query: Optional[QueryInfo] = Field(
        default=None,
        description="Structured query extracted from the question",
    )
    data: Optional[DataInfo] = Field(
        default=None,
        description="Raw data retrieved from the database",
    )


class HealthResponse(BaseModel):
    """
    The response body for GET /health.
    """
    status: str
    app: str
    env: str
    database: str