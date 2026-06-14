from sqlalchemy import Column, Integer, String, Text
from app.models import Base

class QueueOrder(Base):
    __tablename__ = "queue_orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String(10), nullable=False, unique=True)
    customer = Column(String(100), nullable=False)
    order_content = Column(String(200), nullable=False)
    quantity = Column(String(10), nullable=False, default="×1")
    note = Column(Text, default="无备注")
    status = Column(String(20), nullable=False, default="等待中")
