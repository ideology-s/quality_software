from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatMessage(BaseModel):
    id: int
    role: str
    content: str
    thinking: str = ""
