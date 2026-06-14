from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time

class StallLogCreate(BaseModel):
    date: date
    start_time: time
    end_time: time
    location: str
    income: float
    profit: float
    note: Optional[str] = ""

class StallLogUpdate(BaseModel):
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
    income: Optional[float] = None
    profit: Optional[float] = None
    note: Optional[str] = None

class StallLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date: date
    start_time: time
    end_time: time
    location: str
    income: float
    profit: float
    note: str

class WeeklySummary(BaseModel):
    count: int
    total_hours: float
    total_income: float
    total_profit: float

class WeatherCreate(BaseModel):
    temperature: float
    weather_type: str
    is_rainy: bool
    wind_level: int

class WeatherResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date: date
    temperature: float
    weather_type: str
    is_rainy: bool
    wind_level: int

class StallAdviceRequest(BaseModel):
    sleep_hours: float
    work_hours: float
    is_unwell: bool
    planned_stall_hours: float
    location_type: str

class StallAdviceResponse(BaseModel):
    health_status: str
    weather_status: str
    fatigue_status: str
    overall_advice: str
    details: list
    is_recommended: bool
