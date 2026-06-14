from pydantic import BaseModel, ConfigDict
from typing import Optional

class QueueOrderCreate(BaseModel):
    customer: str
    order: str
    quantity: str = "×1"
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

class QueueSummary(BaseModel):
    current_number: Optional[str]
    queue_count: int
    is_crowded: bool
