# app/services/response_service.py
from app.services.llm_service import ask_llm


RESPONSE_SYSTEM_PROMPT = """You are a helpful and professional bank assistant.

Your job is to answer customer questions using the data retrieved from the bank's database.

Rules:
- Give a clear, concise, and natural response in 1-2 sentences
- Always include the actual value in your response
- Be professional but friendly
- Do not make up any information beyond what is provided
- If the data says "None" for collateral, say "no collateral is required"
- For tenure, use proper grammar: "1 year" not "1 years"
- For addresses, say "located at" or "situated at"
- For managers, say "The manager is" or "managed by"
"""


def generate_response(
    original_question: str,
    fact: str,
    attribute: str,
    formatted_value: str,
) -> str:
    """
    Generates a natural language response from a database result.

    Args:
        original_question: The user's original question
        fact: The fact that was queried (e.g. "home_loan")
        attribute: The attribute that was queried (e.g. "interest_rate")
        formatted_value: The formatted value from the database (e.g. "8.5%")

    Returns:
        A natural language response string.

    Example:
        generate_response(
            original_question="What is the home loan interest rate?",
            fact="home_loan",
            attribute="interest_rate",
            formatted_value="8.5%",
        )
        → "The current home loan interest rate is 8.5%."
    """
    prompt = f"""Customer question: {original_question}

Retrieved from database:
- Topic: {fact.replace("_", " ")}
- Field: {attribute.replace("_", " ")}
- Value: {formatted_value}

Generate a natural, professional response to the customer's question using this data."""

    return ask_llm(
        prompt=prompt,
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        temperature=0.3,  # slight creativity for natural language
        max_tokens=150,
    )


def generate_not_found_response(original_question: str) -> str:
    """
    Generates a polite response when no data is found.

    Args:
        original_question: The user's original question

    Returns:
        A polite response explaining the information is not available.
    """
    prompt = f"""Customer question: {original_question}

The database does not contain information to answer this question.
Generate a polite, professional response explaining that you cannot
answer this question and suggest they contact the bank directly."""

    return ask_llm(
        prompt=prompt,
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        temperature=0.3,
        max_tokens=150,
    )


def process_chat(
    db,
    original_question: str,
    search_result: dict,
) -> dict:
    """
    The main function that ties everything together.
    Takes a search result and returns the final chat response.

    Args:
        db: SQLAlchemy session (not used here but passed for consistency)
        original_question: The user's original question
        search_result: Output from search_from_query_result()

    Returns:
        {
            "question": "What is the home loan interest rate?",
            "answer": "The current home loan interest rate is 8.5%.",
            "data": {...},
            "success": True,
        }
    """
    if not search_result["found"]:
        answer = generate_not_found_response(original_question)
        return {
            "question": original_question,
            "answer": answer,
            "data": None,
            "success": False,
        }

    data = search_result["data"]

    answer = generate_response(
        original_question=original_question,
        fact=data["fact"],
        attribute=data["attribute"],
        formatted_value=data["formatted_value"],
    )

    return {
        "question": original_question,
        "answer": answer,
        "data": data,
        "success": True,
    }