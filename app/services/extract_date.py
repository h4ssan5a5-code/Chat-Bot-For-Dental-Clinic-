from app.services.extract_details import extract_details


def extract_date(message: str):

    details = extract_details(message)

    if details:
        return details.get("appointment_date")

    return None