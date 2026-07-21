from app.services.gemini_service import generate_answer


def extract_phone(message: str):

    prompt = f"""
Extract ONLY the phone number.

Rules:
- Return ONLY the phone number.
- No explanation.
- No JSON.
- If none exists return NONE.

Message:

{message}
"""

    response = generate_answer(prompt)

    return response.strip()