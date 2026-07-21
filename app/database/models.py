from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    appointment_date = Column(String)
    appointment_time = Column(String)
    message = Column(String)