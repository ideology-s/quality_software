from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    cost: float
    stock: int
    image: str = ""

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    stock: Optional[int] = None
    image: Optional[str] = None

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float
    cost: float
    stock: int
    sold: int
    image: str

class ProductDetailResponse(ProductResponse):
    income: float
    profit: float
    stock_status: str
    is_loss_sale: bool

class ProductSummary(BaseModel):
    total_income: float
    total_profit: float
    product_count: int
