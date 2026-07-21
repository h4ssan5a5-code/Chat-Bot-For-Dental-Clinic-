import json

from app.services.gemini_service import generate_answer


def extract_details(message: str):
    prompt = f"""
Extract appointment details.

Return ONLY JSON.

Fields:

name
phone
email
appointment_date
appointment_time
message

If missing, return an empty string.

Message:

{message}
"""

    response = generate_answer(prompt)

    try:
        return json.loads(response)
    except:
        return None
    