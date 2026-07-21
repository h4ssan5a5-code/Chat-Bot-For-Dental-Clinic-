from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Appointment
from app.schemas.appointment import AppointmentCreate

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    new_appointment = Appointment(
        name=appointment.name,
        phone=appointment.phone,
        email=appointment.email,
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        message=appointment.message,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "message": "Appointment booked successfully!",
        "id": new_appointment.id
    }