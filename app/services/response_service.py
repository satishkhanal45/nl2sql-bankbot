# app/services/response_service.py
from app.services.llm_service import ask_llm


RESPONSE_SYSTEM_PROMPT = """You are a helpful bank assistant.
Answer the customer's question in one short, direct sentence.
Only state the fact. No extra explanation.

Examples:
Q: What is the home loan interest rate?
A: The home loan interest rate is 8.5%.

Q: Who is the manager of branch anamnagar?
A: The manager of the Anamnagar branch is Ramesh Shrestha.

Q: What are all the home loan details?
A: Here are the home loan details — interest rate: 8.5%, maximum loan amount: NPR 50,000,000, tenure: up to 25 years, processing fee: 0.5%, collateral: property or land.
"""


def generate_response(
    original_question: str,
    fact: str,
    attribute: str,
    formatted_value: str,
) -> str:
    """Generates a natural language response for a specific query."""
    prompt = f"""Customer question: {original_question}

Retrieved from database:
- Topic: {fact.replace("_", " ")}
- Field: {attribute.replace("_", " ")}
- Value: {formatted_value}

Generate a natural, professional response."""

    return ask_llm(
        prompt=prompt,
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        temperature=0.0,
        max_tokens=80,
    )


def generate_broad_response(
    original_question: str,
    fact: str,
    data: list[dict],
) -> str:
    """Generates a natural language response for a broad query."""

    # Build a readable summary of all values
    details = "\n".join([
        f"- {row['attribute'].replace('_', ' ')}: {row['value']}"
        for row in data
    ])

    prompt = f"""Customer question: {original_question}

Retrieved from database — all details about {fact.replace("_", " ")}:
{details}

Generate a clear, concise, professional response summarising all the information."""

    return ask_llm(
        prompt=prompt,
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        temperature=0.0,
        max_tokens=300,
    )


def generate_not_found_response(original_question: str) -> str:
    """Generates a polite response when no data is found."""
    prompt = f"""Customer question: {original_question}

The database does not contain information to answer this question.
Generate a polite, professional response explaining that you cannot
answer this question and suggest they contact the bank directly."""

    return ask_llm(
        prompt=prompt,
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        temperature=0.0,
        max_tokens=100,
    )


def process_chat(
    db,
    original_question: str,
    search_result: dict,
) -> dict:
    """
    Main function — generates the final answer based on query type.

    Specific query → generate_response() — one sentence answer
    Broad query    → generate_broad_response() — full summary
    Not found      → generate_not_found_response() — polite fallback
    """
    if not search_result["found"]:
        answer = generate_not_found_response(original_question)
        return {
            "question": original_question,
            "answer": answer,
            "data": None,
            "success": False,
        }

    query_type = search_result["query_type"]
    query = search_result["query"]

    if query_type == "specific":
        data = search_result["data"]
        answer = generate_response(
            original_question=original_question,
            fact=query["fact"],
            attribute=data["attribute"],
            formatted_value=data["formatted_value"],
        )
    else:
        # broad query
        answer = generate_broad_response(
            original_question=original_question,
            fact=query["fact"],
            data=search_result["data"],
        )

    return {
        "question": original_question,
        "answer": answer,
        "data": search_result["data"],
        "success": True,
    }