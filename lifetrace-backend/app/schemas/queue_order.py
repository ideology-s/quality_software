from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class OrderItem(BaseModel):
    product_id: int
    quantity: int = 1

class QueueOrderCreate(BaseModel):
    customer: str
    items: List[OrderItem]
    note: str = "无备注"

class QueueOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    number: str
    customer: str
    order_content: str
    quantity: str
    note: str
    status: str
    items: list = []
    total_price: float = 0
    total_cost: float = 0
    stall_log_id: Optional[int] = None

class QueueSummary(BaseModel):
    current_number: Optional[str]
    queue_count: int
    is_crowded: bool
