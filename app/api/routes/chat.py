# app/api/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, QueryInfo, DataInfo
from app.services.query_service import understand_query
from app.services.search_service import search_from_query_result
from app.services.response_service import process_chat
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    """
    Main chat endpoint.

    Accepts a natural language question and returns a natural language answer.

    Pipeline:
    1. understand_query() — LLM converts question to structured JSON
    2. search_from_query_result() — searches PostgreSQL
    3. process_chat() — LLM converts result to natural language
    """
    try:
        logger.info(f"Received question: {request.question}")

        # Phase 10: understand the question
        query_result = understand_query(request.question)
        logger.info(f"Query understood: {query_result}")

        # Phase 11: search the database
        search_result = search_from_query_result(db, query_result)
        logger.info(f"Search result found: {search_result['found']}")

        # Phase 12: generate natural language response
        chat_response = process_chat(db, request.question, search_result)
        logger.info(f"Response generated successfully")

        # Build the response
        query_info = QueryInfo(
            entity=query_result.get("entity"),
            fact=query_result.get("fact"),
            attribute=query_result.get("attribute"),
        )

        data_info = None
        if search_result["found"] and search_result["data"]:
            data = search_result["data"]
            data_info = DataInfo(
                value=data.get("value"),
                type=data.get("type"),
                path_name=data.get("path_name"),
                formatted_value=data.get("formatted_value"),
            )

        return ChatResponse(
            question=request.question,
            answer=chat_response["answer"],
            success=chat_response["success"],
            query=query_info,
            data=data_info,
        )

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your question: {str(e)}",
        )