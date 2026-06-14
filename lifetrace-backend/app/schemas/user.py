from pydantic import BaseModel
from datetime import datetime

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    token: str
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime
