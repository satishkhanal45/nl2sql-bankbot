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

BRANCHES:
1. branch_anamnagar → address, phone, email, website, manager, opening_hours, branch_code, province, district, city, atm_available, parking_available
2. branch_baneshwor → address, phone, email, website, manager, opening_hours, branch_code, province, district, city, atm_available, parking_available
3. branch_kalanki   → address, phone, email, website, manager, opening_hours, branch_code, province, district, city, atm_available, parking_available
4. branch_pokhara   → address, phone, email, website, manager, opening_hours, branch_code, province, district, city, atm_available, parking_available

LOANS:
5. home_loan       → interest_rate, minimum_loan_amount, maximum_loan_amount, minimum_tenure, maximum_tenure, processing_fee, collateral, eligibility, required_documents, loan_type
6. education_loan  → interest_rate, minimum_loan_amount, maximum_loan_amount, minimum_tenure, maximum_tenure, processing_fee, collateral, eligibility, required_documents, loan_type
7. personal_loan   → interest_rate, minimum_loan_amount, maximum_loan_amount, minimum_tenure, maximum_tenure, processing_fee, collateral, eligibility, required_documents, loan_type
8. auto_loan       → interest_rate, minimum_loan_amount, maximum_loan_amount, minimum_tenure, maximum_tenure, processing_fee, collateral, eligibility, required_documents, loan_type

DEPOSIT ACCOUNTS:
9.  saving_account   → interest_rate, minimum_deposit, maximum_deposit, currency, interest_calculation, eligibility, required_documents
10. current_account  → interest_rate, minimum_deposit, currency, interest_calculation, eligibility, required_documents, service_charge
11. fixed_deposit    → interest_rate, minimum_deposit, currency, interest_calculation, maturity_period, minimum_tenure, maximum_tenure
12. recurring_deposit → interest_rate, minimum_deposit, currency, interest_calculation, minimum_tenure, maximum_tenure, eligibility

CARDS:
13. debit_card  → annual_fee, joining_fee, cashback, reward_points, replacement_fee, pin_generation, cash_withdrawal_limit, transaction_limit, supported_platforms
14. credit_card → annual_fee, joining_fee, cashback, reward_points, replacement_fee, pin_generation, cash_withdrawal_limit, transaction_limit, supported_platforms, eligibility

SERVICES:
15. mobile_banking   → availability, supported_platforms, transaction_limit, service_charge, registration_requirement
16. internet_banking → availability, supported_platforms, transaction_limit, service_charge, registration_requirement
17. sms_banking      → availability, supported_platforms, transaction_limit, service_charge, registration_requirement
18. qr_payment       → availability, supported_platforms, transaction_limit, service_charge, registration_requirement
19. remittance       → availability, supported_platforms, transaction_limit, service_charge, registration_requirement

ATM:
20. atm_anamnagar  → address, availability, cash_withdrawal_limit, deposit_machine_available, mini_statement, balance_inquiry
21. atm_baneshwor  → address, availability, cash_withdrawal_limit, deposit_machine_available, mini_statement, balance_inquiry

ORGANIZATION:
22. head_office          → address, phone, email, website, manager, swift_code, established_year, total_branches
23. customer_support     → phone, email, toll_free_number, support_hours, availability
24. grievance_department → grievance_email, grievance_phone, resolution_time, support_hours, website
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

IMPORTANT — when to set attribute to null:
- If the user asks for ALL information about a fact
  (e.g. "Tell me everything about home loan",
        "What are all the home loan details?",
        "Give me full details of personal loan")
  → set attribute to null

- If the user asks for a SPECIFIC piece of information
  (e.g. "What is the home loan interest rate?",
        "Who is the manager of branch anamnagar?")
  → set attribute to the exact matching label

- If you cannot determine the fact or attribute, return:
  {{"entity": "bank", "fact": null, "attribute": null}}

Return ONLY the JSON. No explanation. No markdown. No extra text.
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

    Two valid success cases:
    1. Specific query  → fact + attribute both present
    2. Broad query     → fact present, attribute is None
    """
    raw_response = ask_llm(
        prompt=user_question,
        system_prompt=SYSTEM_PROMPT,
        temperature=0.0,
        max_tokens=100,
    )

    parsed = extract_json_from_response(raw_response)

    if parsed is None:
        return {
            "entity": "bank",
            "fact": None,
            "attribute": None,
            "original_question": user_question,
            "query_type": "unknown",
            "success": False,
            "error": f"Could not parse LLM response: {raw_response}",
        }

    fact = parsed.get("fact")
    attribute = parsed.get("attribute")

    # Complete failure — fact not identified
    if not fact or fact == "null":
        return {
            "entity": "bank",
            "fact": None,
            "attribute": None,
            "original_question": user_question,
            "query_type": "unknown",
            "success": False,
            "error": "Question not understood — fact could not be identified",
        }

    # Broad query — fact found but attribute is null
    if not attribute or attribute == "null":
        return {
            "entity": parsed.get("entity", "bank"),
            "fact": fact,
            "attribute": None,
            "original_question": user_question,
            "query_type": "broad",
            "success": True,
        }

    # Specific query — both fact and attribute found
    return {
        "entity": parsed.get("entity", "bank"),
        "fact": fact,
        "attribute": attribute,
        "original_question": user_question,
        "query_type": "specific",
        "success": True,
    }