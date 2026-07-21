from app.services.gemini_service import generate_answer


def extract_name(message: str):

    prompt = f"""
Extract ONLY the person's full name.

Rules:
- Return ONLY the name.
- No explanation.
- No JSON.
- If no name exists, return NONE.

Message:

{message}
"""

    response = generate_answer(prompt)

    return response.strip()