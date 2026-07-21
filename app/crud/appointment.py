from sqlalchemy.orm import Session
from app.database.models import Appointment
from app.schemas.appointment import AppointmentCreate


def create_appointment(db: Session, appointment: AppointmentCreate):
    db_appointment = Appointment(
        name=appointment.name,
        phone=appointment.phone,
        email=appointment.email,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        message=appointment.message,
    )

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment