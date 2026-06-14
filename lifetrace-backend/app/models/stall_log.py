from sqlalchemy import Column, Integer, Float, String, Date, Time, Text
from app.models import Base

class StallLog(Base):
    __tablename__ = "stall_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String(200), nullable=False)
    income = Column(Float, nullable=False, default=0)
    profit = Column(Float, nullable=False, default=0)
    note = Column(Text, default="")
