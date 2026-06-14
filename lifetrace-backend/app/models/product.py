from sqlalchemy import Column, Integer, Float, String, Text
from app.models import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False, default=0)
    cost = Column(Float, nullable=False, default=0)
    stock = Column(Integer, nullable=False, default=0)
    sold = Column(Integer, nullable=False, default=0)
    image = Column(Text, default="")
