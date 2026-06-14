from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import ai_service, summary_service
from app.schemas.ai import ChatRequest, ChatMessage
from app.schemas.common import ApiResponse
router = APIRouter(tags=["AI助手"])

@router.post("/ai/chat", response_model=ApiResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    if not request.message.strip():
        return ApiResponse(code=400, message="消息不能为空")
    result = ai_service.chat_with_ai(request.message)
    return ApiResponse(data=result)

@router.get("/summary/today", response_model=ApiResponse)
def today_summary(db: Session = Depends(get_db)):
    data = summary_service.get_today_summary(db)
    return ApiResponse(data=data)
