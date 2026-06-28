# app/services/query_service.py
import json
import re
from typing import Optional
from app.services.llm_service import ask_llm


# This is the full list of entities, facts, and attributes
# the LLM needs to know about so it maps questions correctly.
# We give it this context so it doesn't guess wrong values.
DATABASE_CONTEXT = """
You have access to a bank knowledge database with the following structure:

ENTITY: bank
FACTS and their ATTRIBUTES:

1. central_bank
   - address, email, phone, website, manager

2. home_loan
   - interest_rate, loan_amount, tenure, address, processing_fee, collateral

3. main_branch
   - address, email, phone, manager, website

4. saving_account
   - interest_rate, minimum_balance, maximum_balance

5. fixed_deposit
   - interest_rate, minimum_balance, tenure

6. sub_branch
   - address, email, phone, manager

7. personal_loan
   - interest_rate, loan_amount, tenure, processing_fee, collateral, loan_type

8. vehicle_loan
   - interest_rate, loan_amount, tenure, processing_fee, collateral, loan_type
"""


SYSTEM_PROMPT = f"""You are a structured data extractor for a bank knowledge base.

{DATABASE_CONTEXT}

Your job:
- Read the user's question
- Identify which entity, fact, and attribute they are asking about
- Return ONLY a valid JSON object with exactly these three keys:
  {{"entity": "...", "fact": "...", "attribute": "..."}}

Rules:
- entity is always "bank"
- fact must exactly match one of the facts listed above
- attribute must exactly match one of the attributes listed above
- If you cannot determine the fact or attribute, return:
  {{"entity": "bank", "fact": null, "attribute": null}}
- Return ONLY the JSON. No explanation. No markdown. No extra text.
"""


def extract_json_from_response(response: str) -> Optional[dict]:
    """
    Safely parses the LLM response into a Python dict.

    Handles edge cases where the model adds:
    - Markdown code blocks: ```json ... ```
    - Extra whitespace or newlines
    - Partial JSON

    Returns None if parsing fails.
    """
    # Remove markdown code blocks if present
    response = response.strip()
    response = re.sub(r"```json\s*", "", response)
    response = re.sub(r"```\s*", "", response)
    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to find JSON object inside the response
        match = re.search(r"\{.*?\}", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None
    return None


def understand_query(user_question: str) -> dict:
    """
    Converts a natural language question into structured JSON.

    Args:
        user_question: The user's question in plain English

    Returns:
        A dict with keys: entity, fact, attribute
        Example:
        {
            "entity": "bank",
            "fact": "home_loan",
            "attribute": "interest_rate",
            "original_question": "What is the home loan interest rate?",
            "success": True,
        }

    If understanding fails:
        {
            "entity": "bank",
            "fact": None,
            "attribute": None,
            "original_question": "...",
            "success": False,
            "error": "Could not parse response"
        }
    """
    raw_response = ask_llm(
        prompt=user_question,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.0,  # fully deterministic for structured output
        max_tokens=100,   # JSON is short — no need for more
    )

    parsed = extract_json_from_response(raw_response)

    if parsed is None:
        return {
            "entity": "bank",
            "fact": None,
            "attribute": None,
            "original_question": user_question,
            "success": False,
            "error": f"Could not parse LLM response: {raw_response}",
        }

    fact = parsed.get("fact")
    attribute = parsed.get("attribute")

    if not fact or not attribute or fact == "null" or attribute == "null":
        return {
            "entity": "bank",
            "fact": None,
            "attribute": None,
            "original_question": user_question,
            "success": False,
            "error": "Question not understood — fact or attribute is missing",
        }

    return {
        "entity": parsed.get("entity", "bank"),
        "fact": fact,
        "attribute": attribute,
        "original_question": user_question,
        "success": True,
    }