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

CATEGORIES, INSTANCES, and their ATTRIBUTES:

CATEGORY: branch
  INSTANCES: anamnagar, baneshwor, kalanki, pokhara
  ATTRIBUTES: address, phone, email, website, manager, opening_hours,
              branch_code, province, district, city, atm_available, parking_available

CATEGORY: loan
  INSTANCES: home_loan, education_loan, personal_loan, auto_loan
  ATTRIBUTES: interest_rate, minimum_loan_amount, maximum_loan_amount,
              minimum_tenure, maximum_tenure, processing_fee, collateral,
              eligibility, required_documents, loan_type

CATEGORY: account
  INSTANCES: saving_account, current_account, fixed_deposit, recurring_deposit
  ATTRIBUTES: interest_rate, minimum_deposit, maximum_deposit, currency,
              interest_calculation, maturity_period, eligibility,
              required_documents, service_charge

CATEGORY: card
  INSTANCES: debit_card, credit_card
  ATTRIBUTES: annual_fee, joining_fee, cashback, reward_points,
              replacement_fee, pin_generation, cash_withdrawal_limit,
              transaction_limit, supported_platforms, eligibility

CATEGORY: service
  INSTANCES: mobile_banking, internet_banking, sms_banking, qr_payment, remittance
  ATTRIBUTES: availability, supported_platforms, transaction_limit,
              service_charge, registration_requirement

CATEGORY: atm
  INSTANCES: atm_anamnagar, atm_baneshwor
  ATTRIBUTES: address, availability, cash_withdrawal_limit,
              deposit_machine_available, mini_statement, balance_inquiry

CATEGORY: organization
  INSTANCES: head_office, customer_support, grievance_department
  ATTRIBUTES: address, phone, email, website, manager, swift_code,
              established_year, total_branches, toll_free_number,
              support_hours, grievance_email, grievance_phone,
              resolution_time, availability
"""


SYSTEM_PROMPT = f"""You are a structured data extractor for a bank knowledge base.

{DATABASE_CONTEXT}

Your job:
- Read the user question
- Identify the category, instance, and attribute being asked about
- Return ONLY a valid JSON object with exactly these four keys:
  {{"entity": "bank", "fact": "<category>", "instance": "<instance>", "attribute": "<attribute>"}}

Rules:
- entity is always "bank"
- fact must exactly match one of the CATEGORY names listed above
- instance must exactly match one of the INSTANCE names listed above
- attribute must exactly match one of the ATTRIBUTE names listed above

IMPORTANT — when to set attribute to null:
- If the user asks for ALL information about an instance
  (e.g. "Tell me everything about home loan",
        "Give me full details of anamnagar branch")
  → set attribute to null, keep fact and instance

- If the user asks about an entire CATEGORY
  (e.g. "Tell me all loan types", "What branches do you have?")
  → set attribute to null AND instance to null, keep fact only

- If you cannot determine the category, return:
  {{"entity": "bank", "fact": null, "instance": null, "attribute": null}}

Return ONLY the JSON. No explanation. No markdown. No extra text.

Examples:
Q: What is the home loan interest rate?
A: {{"entity": "bank", "fact": "loan", "instance": "home_loan", "attribute": "interest_rate"}}

Q: Tell me everything about the anamnagar branch
A: {{"entity": "bank", "fact": "branch", "instance": "anamnagar", "attribute": null}}

Q: What loans do you offer?
A: {{"entity": "bank", "fact": "loan", "instance": null, "attribute": null}}

Q: What is the toll free number for customer support?
A: {{"entity": "bank", "fact": "organization", "instance": "customer_support", "attribute": "toll_free_number"}}
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

    Three valid success cases:
    1. Specific query  → fact + instance + attribute all present
    2. Instance broad  → fact + instance present, attribute is None
    3. Category broad  → fact only present, instance and attribute are None
    """
    raw_response = ask_llm(
        prompt=user_question,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.0,
        max_tokens=150,
    )

    parsed = extract_json_from_response(raw_response)

    if parsed is None:
        return {
            "entity": "bank",
            "fact": None,
            "instance": None,
            "attribute": None,
            "original_question": user_question,
            "query_type": "unknown",
            "success": False,
            "error": f"Could not parse LLM response: {raw_response}",
        }

    fact = parsed.get("fact")
    instance = parsed.get("instance")
    attribute = parsed.get("attribute")

    # Complete failure — category not identified
    if not fact or fact == "null":
        return {
            "entity": "bank",
            "fact": None,
            "instance": None,
            "attribute": None,
            "original_question": user_question,
            "query_type": "unknown",
            "success": False,
            "error": "Question not understood — category could not be identified",
        }

    # Clean up null strings
    instance = None if (not instance or instance == "null") else instance
    attribute = None if (not attribute or attribute == "null") else attribute

    # Determine query type
    if instance and attribute:
        query_type = "specific"
    elif instance and not attribute:
        query_type = "broad_instance"
    else:
        query_type = "broad_category"

    return {
        "entity": parsed.get("entity", "bank"),
        "fact": fact,
        "instance": instance,
        "attribute": attribute,
        "original_question": user_question,
        "query_type": query_type,
        "success": True,
    }