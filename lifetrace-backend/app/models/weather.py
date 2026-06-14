from sqlalchemy import Column, Integer, Float, String, Date, Boolean
from app.models import Base

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False, unique=True)
    temperature = Column(Float, nullable=False)
    weather_type = Column(String(50), nullable=False)
    is_rainy = Column(Boolean, nullable=False, default=False)
    wind_level = Column(Integer, nullable=False, default=0)
