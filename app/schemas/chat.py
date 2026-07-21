from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    session_id: Optional[str] = "default"
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]