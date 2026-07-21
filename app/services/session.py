from collections import defaultdict

# Stores session data in memory
sessions = defaultdict(lambda: {
    "history": [],
    "state": "IDLE",
    "booking": {
        "name": None,
        "phone": None,
        "email": None,
        "appointment_date": None,
        "appointment_time": None,
        "message": None
    }
})


# -----------------------------
# Conversation History
# -----------------------------

def add_message(session_id: str, role: str, message: str):
    sessions[session_id]["history"].append({
        "role": role,
        "message": message
    })


def get_history(session_id: str):
    return sessions[session_id]["history"]


def clear_history(session_id: str):
    sessions[session_id]["history"] = []


# -----------------------------
# Booking
# -----------------------------

def get_booking(session_id: str):
    return sessions[session_id]["booking"]


def update_booking(session_id: str, data: dict):
    booking = sessions[session_id]["booking"]

    for key, value in data.items():

        if value is None:
            continue

        if isinstance(value, str) and value.strip() == "":
            continue

        booking[key] = value


def clear_booking(session_id: str):
    sessions[session_id]["booking"] = {
        "name": None,
        "phone": None,
        "email": None,
        "appointment_date": None,
        "appointment_time": None,
        "message": None
    }


# -----------------------------
# Workflow State
# -----------------------------

def get_state(session_id: str):
    return sessions[session_id]["state"]


def set_state(session_id: str, state: str):
    sessions[session_id]["state"] = state