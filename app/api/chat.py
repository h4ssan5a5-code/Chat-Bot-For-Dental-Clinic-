from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.chatbot import ask_chatbot
from app.schemas.chat import ChatRequest

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    answer = ask_chatbot(request.message,request.session_id,db)

    return {
        "response": answer
    }
