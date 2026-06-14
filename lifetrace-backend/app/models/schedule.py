from sqlalchemy import Column, Integer, String, Date, Time, Boolean
from app.models import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    start = Column(Time, nullable=False)
    end = Column(Time, nullable=False)
    task = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="待办")
