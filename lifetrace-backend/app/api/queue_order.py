from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import queue_service
from app.schemas.queue_order import QueueOrderCreate, QueueOrderResponse, QueueSummary
from app.schemas.common import ApiResponse
router = APIRouter(tags=["排队取号"])

@router.get("/queue", response_model=ApiResponse)
def list_queue(db: Session = Depends(get_db)):
    data = queue_service.get_queue_list(db)
    return ApiResponse(data=data)

@router.get("/queue/summary", response_model=ApiResponse)
def queue_summary(db: Session = Depends(get_db)):
    data = queue_service.get_queue_summary(db)
    return ApiResponse(data=data)

@router.post("/queue", response_model=ApiResponse)
def take_number(data: QueueOrderCreate, db: Session = Depends(get_db)):
    result = queue_service.take_number(db, data)
    if isinstance(result, dict) and "error" in result:
        return ApiResponse(code=409, message=result["error"])
    return ApiResponse(data=QueueOrderResponse.model_validate(result))

@router.put("/queue/{number}/serve", response_model=ApiResponse)
def serve_next(number: str, db: Session = Depends(get_db)):
    result = queue_service.serve_next(db)
    if isinstance(result, dict) and "error" in result:
        return ApiResponse(code=400, message=result["error"])
    return ApiResponse(data=QueueOrderResponse.model_validate(result))

@router.put("/queue/{number}/complete", response_model=ApiResponse)
def complete_order(number: str, db: Session = Depends(get_db)):
    order = queue_service.complete_order(db, number)
    if not order:
        return ApiResponse(code=404, message="排队订单不存在")
    return ApiResponse(data=QueueOrderResponse.model_validate(order))

@router.put("/queue/{number}/cancel", response_model=ApiResponse)
def cancel_order(number: str, db: Session = Depends(get_db)):
    order = queue_service.cancel_order(db, number)
    if not order:
        return ApiResponse(code=404, message="排队订单不存在")
    return ApiResponse(data=QueueOrderResponse.model_validate(order))

@router.delete("/queue/{number}", response_model=ApiResponse)
def delete_order(number: str, db: Session = Depends(get_db)):
    ok = queue_service.delete_order(db, number)
    if not ok:
        return ApiResponse(code=404, message="排队订单不存在")
    return ApiResponse(message="删除成功")
