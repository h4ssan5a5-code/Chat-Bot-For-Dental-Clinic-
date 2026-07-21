from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class AppointmentRequest(BaseModel):
    name: str
    phone: str
    preferred_date: str
    preferred_time: str

class AppointmentCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    appointment_date: str
    appointment_time: str
    message: str




