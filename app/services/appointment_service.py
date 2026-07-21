from sqlalchemy.orm import Session
from app.database.models import Appointment


def save_appointment(db: Session, data: dict):
    appointment = Appointment(
        name=data.get("name", ""),
        phone=data.get("phone", ""),
        email=data.get("email", ""),
        appointment_date=data.get("appointment_date", ""),
        appointment_time=data.get("appointment_time", ""),
        message=data.get("message", ""),
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment