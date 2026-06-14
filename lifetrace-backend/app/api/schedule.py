from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.services import schedule_service
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse, ScheduleSummary
from app.schemas.common import ApiResponse
router = APIRouter(tags=["日程清单"])

@router.get("/schedules", response_model=ApiResponse)
def list_schedules(db: Session = Depends(get_db)):
    items = schedule_service.get_schedules(db)
    return ApiResponse(data=[ScheduleResponse.model_validate(s) for s in items])

@router.get("/schedules/summary", response_model=ApiResponse)
def schedule_summary(db: Session = Depends(get_db)):
    data = schedule_service.get_schedule_summary(db)
    return ApiResponse(data=data)

@router.get("/schedules/date/{target_date}", response_model=ApiResponse)
def list_schedules_by_date(target_date: date, db: Session = Depends(get_db)):
    items = schedule_service.get_schedules_by_date(db, target_date)
    return ApiResponse(data=[ScheduleResponse.model_validate(s) for s in items])

@router.post("/schedules", response_model=ApiResponse)
def create_schedule(data: ScheduleCreate, db: Session = Depends(get_db)):
    item = schedule_service.create_schedule(db, data)
    return ApiResponse(data=ScheduleResponse.model_validate(item))

@router.put("/schedules/{schedule_id}", response_model=ApiResponse)
def update_schedule(schedule_id: int, data: ScheduleUpdate, db: Session = Depends(get_db)):
    item = schedule_service.update_schedule(db, schedule_id, data)
    if not item:
        return ApiResponse(code=404, message="日程不存在")
    return ApiResponse(data=ScheduleResponse.model_validate(item))

@router.delete("/schedules/{schedule_id}", response_model=ApiResponse)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    ok = schedule_service.delete_schedule(db, schedule_id)
    if not ok:
        return ApiResponse(code=404, message="日程不存在")
    return ApiResponse(message="删除成功")
