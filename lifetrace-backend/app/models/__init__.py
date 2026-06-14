from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from .stall_log import StallLog
from .weather import Weather
from .schedule import Schedule
from .product import Product
from .queue_order import QueueOrder
from .user import User

__all__ = ["Base", "StallLog", "Weather", "Schedule", "Product", "QueueOrder", "User"]
