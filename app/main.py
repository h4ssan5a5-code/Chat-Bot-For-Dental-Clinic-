from fastapi import FastAPI

from app.database.database import Base, engine

# Import models so SQLAlchemy knows about them
from app.database import models

from app.api.chat import router as chat_router
from app.api.appointment import router as appointment_router


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rashid Dental AI Assistant"
)

app.include_router(chat_router)
app.include_router(appointment_router)