from sqlalchemy.orm import Session

from app.rag.vectorstore import VectorStore
from app.services.gemini_service import generate_answer
from app.services.intent_detector import detect_booking_intent
from app.services.appointment_service import save_appointment

from app.services.extract_name import extract_name
from app.services.extract_phone import extract_phone
from app.services.extract_date import extract_date
from app.services.extract_time import extract_time

from app.services.session import (
    get_booking,
    update_booking,
    clear_booking,
    get_state,
    set_state,
)

# Build vector store once
vector_store = VectorStore()
vector_store.build()


def ask_chatbot(question: str, session_id: str, db: Session):

    state = get_state(session_id)

    # ==================================================
    # START BOOKING
    # ==================================================

    if state == "IDLE" and detect_booking_intent(question):
        clear_booking(session_id)
        set_state(session_id, "WAITING_NAME")

        return (
            "Sure! I'd be happy to help you book an appointment.\n\n"
            "What is your full name?"
        )

    # ==================================================
    # WAITING FOR NAME
    # ==================================================

    if state == "WAITING_NAME":

        name = extract_name(question)

        if not name or name.upper() == "NONE":
            return "I couldn't understand your name. Please tell me your full name."

        update_booking(session_id, {
            "name": name
        })

        set_state(session_id, "WAITING_PHONE")

        return "Great! What is your phone number?"

    # ==================================================
    # WAITING FOR PHONE
    # ==================================================

    if state == "WAITING_PHONE":

        phone = extract_phone(question)

        if not phone or phone.upper() == "NONE":
            return "I couldn't understand your phone number. Please enter it again."

        update_booking(session_id, {
            "phone": phone
        })

        set_state(session_id, "WAITING_DATE")

        return "What date would you like to book your appointment?"

    # ==================================================
    # WAITING FOR DATE
    # ==================================================

    if state == "WAITING_DATE":

        appointment_date = extract_date(question)

        if not appointment_date:
            return "I couldn't understand the appointment date. Please enter it again."

        update_booking(session_id, {
            "appointment_date": appointment_date
        })

        set_state(session_id, "WAITING_TIME")

        return "What time would you prefer?"

    # ==================================================
    # WAITING FOR TIME
    # ==================================================

    if state == "WAITING_TIME":

        appointment_time = extract_time(question)

        if not appointment_time:
            return "I couldn't understand the appointment time. Please enter it again."

        update_booking(session_id, {
            "appointment_time": appointment_time
        })

        booking = get_booking(session_id)

        save_appointment(db, booking)

        clear_booking(session_id)
        set_state(session_id, "IDLE")

        return (
            "✅ Appointment booked successfully!\n\n"
            f"Name: {booking['name']}\n"
            f"Phone: {booking['phone']}\n"
            f"Date: {booking['appointment_date']}\n"
            f"Time: {booking['appointment_time']}"
        )

    # ==================================================
    # RAG QUESTION ANSWERING
    # ==================================================

    results = vector_store.search(question)

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
You are Rashid Dental Clinic's AI Assistant.

Answer ONLY using the clinic information below.

Context:
{context}

Question:
{question}
"""

    return generate_answer(prompt)