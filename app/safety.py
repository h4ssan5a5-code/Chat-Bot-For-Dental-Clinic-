DIAGNOSIS_KEYWORDS = [
    "diagnose",
    "diagnosis",
    "what disease",
    "what is wrong",
    "what do i have",
]

MEDICATION_KEYWORDS = [
    "medicine",
    "medication",
    "antibiotic",
    "painkiller",
    "prescription",
    "drug",
]

EMERGENCY_KEYWORDS = [
    "bleeding",
    "can't breathe",
    "cannot breathe",
    "swelling",
    "severe pain",
    "unconscious",
    "accident",
]


def check_safety(question: str):
    q = question.lower()

    for word in DIAGNOSIS_KEYWORDS:
        if word in q:
            return (
                False,
                "I'm an AI assistant and cannot diagnose medical conditions. "
                "Please book an appointment with one of our dentists for a professional evaluation."
            )

    for word in MEDICATION_KEYWORDS:
        if word in q:
            return (
                False,
                "I cannot recommend medications or prescribe treatment. "
                "Please consult one of our dentists."
            )

    for word in EMERGENCY_KEYWORDS:
        if word in q:
            return (
                False,
                "Your message may describe a dental emergency. "
                "Please contact Rashid Dental Clinic immediately or visit your nearest emergency department if the situation is severe."
            )

    return True, None