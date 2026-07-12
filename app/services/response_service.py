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
A: Here are the home loan details — interest rate: 8.5%, maximum loan
   amount: NPR 50,000,000, tenure: up to 25 years, processing fee: 0.5%.
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
    details = "\n".join([
        f"- {row['attribute'].replace('_', ' ')}: {row['value']}"
        for row in data
    ])

    prompt = f"""Customer question: {original_question}

Retrieved from database — all details about {fact.replace("_", " ")}:
{details}

Generate a clear, concise, professional response summarising
all the information."""

    return ask_llm(
        prompt=prompt,
        system_prompt=RESPONSE_SYSTEM_PROMPT,
        temperature=0.0,
        max_tokens=300,
    )


def generate_attribute_only_response(
    original_question: str,
    attribute: str,
    data: list[dict],
) -> str:
    """
    Generates a response when the user asks about an attribute
    without specifying a product — e.g. "Give me the interest rate".

    Groups results by category before sending to LLM so the
    response is structured and readable.
    """
    # Group results by category
    grouped: dict[str, list[str]] = {}
    for row in data:
        category = row.get("category", "other")
        # Extract instance name from path
        # path format: bank.<category>.<instance>.<attribute>
        parts = row["path_name"].split(".")
        instance = parts[2] if len(parts) >= 4 else "unknown"
        formatted = row.get("formatted_value", row["value"])
        label = f"{instance.replace('_', ' ')}: {formatted}"

        if category not in grouped:
            grouped[category] = []
        grouped[category].append(label)

    # Build readable summary
    summary_lines = []
    for category, items in grouped.items():
        summary_lines.append(
            f"{category.replace('_', ' ').title()}: {', '.join(items)}"
        )
    summary = "\n".join(summary_lines)

    prompt = f"""Customer question: {original_question}

The customer asked about "{attribute.replace('_', ' ')}" without specifying
a particular product. Here are all available values grouped by category:

{summary}

Generate a clear, professional response listing all the values.
Group them by category in your answer."""

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
    Main function — routes to the correct response generator
    based on query type.

    specific:       → generate_response()
    broad:          → generate_broad_response()
    attribute_only: → generate_attribute_only_response()
    not found:      → generate_not_found_response()
    """
    if not search_result["found"]:
        answer = generate_not_found_response(original_question)
        return {
            "question": original_question,
            "answer":   answer,
            "data":     None,
            "success":  False,
        }

    query_type = search_result["query_type"]
    query      = search_result["query"]

    if query_type == "specific":
        data = search_result["data"]
        answer = generate_response(
            original_question=original_question,
            fact=f"{query.get('fact', '')} {query.get('instance', '')}".strip(),
            attribute=data["attribute"],
            formatted_value=data["formatted_value"],
        )

    elif query_type == "attribute_only":
        answer = generate_attribute_only_response(
            original_question=original_question,
            attribute=query["attribute"],
            data=search_result["data"],
        )

    else:
        # broad_instance or broad_category
        fact_label = query.get("fact", "")
        if query.get("instance"):
            fact_label = f"{fact_label} {query['instance']}"
        answer = generate_broad_response(
            original_question=original_question,
            fact=fact_label,
            data=search_result["data"],
        )

    return {
        "question": original_question,
        "answer":   answer,
        "data":     search_result["data"],
        "success":  True,
    }