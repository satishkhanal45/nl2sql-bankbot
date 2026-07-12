# app/services/query_service.py
import json
import re
from typing import Optional
from app.services.llm_service import ask_llm


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

IMPORTANT — when to set fields to null:

Case 1 — SPECIFIC query (fact + instance + attribute all known):
  Q: "What is the home loan interest rate?"
  A: {{"entity": "bank", "fact": "loan", "instance": "home_loan", "attribute": "interest_rate"}}

Case 2 — BROAD INSTANCE query (fact + instance known, attribute unknown):
  Q: "Tell me everything about home loan"
  A: {{"entity": "bank", "fact": "loan", "instance": "home_loan", "attribute": null}}

Case 3 — BROAD CATEGORY query (only fact known):
  Q: "What loans do you offer?"
  A: {{"entity": "bank", "fact": "loan", "instance": null, "attribute": null}}

Case 4 — ATTRIBUTE ONLY query (only attribute known, no specific product mentioned):
  Q: "Give me the interest rate" or "What are all the interest rates?"
  Q: "What is the processing fee?" or "Show me all processing fees"
  Q: "What are the opening hours?" or "Give me manager details"
  A: {{"entity": "bank", "fact": null, "instance": null, "attribute": "<attribute_label>"}}
  → Use this when the user asks about an attribute WITHOUT specifying
    which product, branch, or service they mean.

Case 5 — UNKNOWN (cannot determine anything):
  A: {{"entity": "bank", "fact": null, "instance": null, "attribute": null}}

Return ONLY the JSON. No explanation. No markdown. No extra text.
"""


def extract_json_from_response(response: str) -> Optional[dict]:
    """
    Safely parses the LLM response into a Python dict.
    Handles markdown code blocks, extra whitespace, and partial JSON.
    """
    response = response.strip()
    response = re.sub(r"```json\s*", "", response)
    response = re.sub(r"```\s*", "", response)
    response = response.strip()

    try:
        return json.loads(response)
    except json.JSONDecodeError:
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

    Five valid cases:
    1. specific        → fact + instance + attribute all present
    2. broad_instance  → fact + instance present, attribute None
    3. broad_category  → fact only present, instance and attribute None
    4. attribute_only  → attribute only present, fact and instance None
    5. unknown         → nothing identified → failure
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

    fact      = parsed.get("fact")
    instance  = parsed.get("instance")
    attribute = parsed.get("attribute")

    # Clean up null strings from LLM
    fact      = None if (not fact      or fact      == "null") else fact
    instance  = None if (not instance  or instance  == "null") else instance
    attribute = None if (not attribute or attribute == "null") else attribute

    # Case 4 — attribute only (no fact, no instance, but attribute present)
    if attribute and not fact and not instance:
        return {
            "entity": parsed.get("entity", "bank"),
            "fact": None,
            "instance": None,
            "attribute": attribute,
            "original_question": user_question,
            "query_type": "attribute_only",
            "success": True,
        }

    # Case 5 — complete failure, nothing identified
    if not fact:
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

    # Case 1, 2, 3 — determine query type from what's present
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