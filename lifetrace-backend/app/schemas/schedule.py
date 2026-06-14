from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time

class ScheduleCreate(BaseModel):
    date: date
    start: time
    end: time
    task: str
    status: str = "待办"

class ScheduleUpdate(BaseModel):
    date: Optional[date] = None
    start: Optional[time] = None
    end: Optional[time] = None
    task: Optional[str] = None
    status: Optional[str] = None

class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date: date
    start: time
    end: time
    task: str
    status: str

class ScheduleSummary(BaseModel):
    pending_count: int
    completed_count: int
    total_count: int
