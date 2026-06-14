from pydantic import BaseModel
from typing import Any

class ApiResponse(BaseModel):
    code: int = 200
    message: str = "ok"
    data: Any = None
