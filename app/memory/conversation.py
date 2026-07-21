conversation_memory = {}


def save_message(user_id, role, message):
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []

    conversation_memory[user_id].append({
        "role": role,
        "message": message
    })


def get_history(user_id):
    return conversation_memory.get(user_id, [])