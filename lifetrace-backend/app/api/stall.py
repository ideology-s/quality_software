from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import stall_service
from app.schemas.stall_log import (
    StallLogCreate, StallLogUpdate, StallLogResponse,
    WeeklySummary, WeatherCreate, WeatherResponse,
    StallAdviceRequest, StallAdviceResponse,
    StartStallRequest, EndStallRequest,
)
from app.schemas.common import ApiResponse
router = APIRouter(tags=["出摊日志"])

@router.get("/stall-logs", response_model=ApiResponse)
def list_stall_logs(db: Session = Depends(get_db)):
    logs = stall_service.get_stall_logs(db)
    return ApiResponse(data=[StallLogResponse.model_validate(log) for log in logs])

@router.post("/stall-logs", response_model=ApiResponse)
def create_stall_log(data: StallLogCreate, db: Session = Depends(get_db)):
    log = stall_service.create_stall_log(db, data)
    return ApiResponse(data=StallLogResponse.model_validate(log))

@router.post("/stall-logs/start", response_model=ApiResponse)
def start_stall(data: StartStallRequest, db: Session = Depends(get_db)):
    log = stall_service.start_stall(db, data.location)
    if not log:
        return ApiResponse(code=409, message="已有出摊在进行中，请先结束当前出摊")
    return ApiResponse(data=StallLogResponse.model_validate(log))

@router.put("/stall-logs/{log_id}/end", response_model=ApiResponse)
def end_stall(log_id: int, data: EndStallRequest = None, db: Session = Depends(get_db)):
    note = data.note if data else ""
    log = stall_service.end_stall(db, log_id, note)
    if not log:
        return ApiResponse(code=404, message="出摊记录不存在或已结束")
    return ApiResponse(data=StallLogResponse.model_validate(log))

@router.get("/stall-logs/active", response_model=ApiResponse)
def active_stall(db: Session = Depends(get_db)):
    log = stall_service.get_active_stall(db)
    if not log:
        return ApiResponse(data=None)
    return ApiResponse(data=StallLogResponse.model_validate(log))

@router.put("/stall-logs/{log_id}", response_model=ApiResponse)
def update_stall_log(log_id: int, data: StallLogUpdate, db: Session = Depends(get_db)):
    log = stall_service.update_stall_log(db, log_id, data)
    if not log:
        return ApiResponse(code=404, message="出摊日志不存在")
    return ApiResponse(data=StallLogResponse.model_validate(log))

@router.delete("/stall-logs/{log_id}", response_model=ApiResponse)
def delete_stall_log(log_id: int, db: Session = Depends(get_db)):
    ok = stall_service.delete_stall_log(db, log_id)
    if not ok:
        return ApiResponse(code=404, message="出摊日志不存在")
    return ApiResponse(message="删除成功")

@router.get("/stall-logs/weekly-summary", response_model=ApiResponse)
def weekly_summary(db: Session = Depends(get_db)):
    data = stall_service.get_weekly_summary(db)
    return ApiResponse(data=data)

@router.post("/weather", response_model=ApiResponse)
def set_weather(data: WeatherCreate, db: Session = Depends(get_db)):
    record = stall_service.set_weather(db, data)
    return ApiResponse(data=WeatherResponse.model_validate(record))

@router.get("/weather/today", response_model=ApiResponse)
def today_weather(db: Session = Depends(get_db)):
    record = stall_service.get_today_weather(db)
    if not record:
        return ApiResponse(code=404, message="暂无今日天气数据")
    return ApiResponse(data=WeatherResponse.model_validate(record))

@router.post("/stall-advice", response_model=ApiResponse)
def stall_advice(data: StallAdviceRequest, db: Session = Depends(get_db)):
    result = stall_service.get_stall_advice(
        db, data.sleep_hours, data.work_hours,
        data.is_unwell, data.planned_stall_hours, data.location_type,
    )
    return ApiResponse(data=result)
