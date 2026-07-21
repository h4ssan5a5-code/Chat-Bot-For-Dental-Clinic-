from app.services.extract_details import extract_details


def extract_time(message: str):

    details = extract_details(message)

    if details:
        return details.get("appointment_time")

    return None