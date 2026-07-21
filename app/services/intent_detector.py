BOOKING_KEYWORDS = [
    "appointment",
    "book",
    "booking",
    "schedule",
    "reserve",
    "visit",
    "see the dentist",
]


def detect_booking_intent(message: str) -> bool:
    message = message.lower()

    return any(keyword in message for keyword in BOOKING_KEYWORDS)