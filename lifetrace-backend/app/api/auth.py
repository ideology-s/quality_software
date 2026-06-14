from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, create_token
from app.schemas.user import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.common import ApiResponse

router = APIRouter(tags=["认证"])

@router.post("/auth/register", response_model=ApiResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if not data.username.strip() or not data.password.strip():
        return ApiResponse(code=400, message="用户名和密码不能为空")

    if len(data.password) < 6:
        return ApiResponse(code=400, message="密码长度不能少于 6 位")

    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        return ApiResponse(code=409, message="用户名已存在")

    user = User(username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id, user.username)
    return ApiResponse(data=TokenResponse(token=token, username=user.username))

@router.post("/auth/login", response_model=ApiResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    if not data.username.strip() or not data.password.strip():
        return ApiResponse(code=400, message="用户名和密码不能为空")

    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        return ApiResponse(code=401, message="用户名或密码错误")

    token = create_token(user.id, user.username)
    return ApiResponse(data=TokenResponse(token=token, username=user.username))
