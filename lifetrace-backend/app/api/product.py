from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import product_service
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductDetailResponse, ProductSummary
from app.schemas.common import ApiResponse
from pydantic import BaseModel

class SellRequest(BaseModel):
    quantity: int

router = APIRouter(tags=["小摊商品"])

@router.get("/products", response_model=ApiResponse)
def list_products(db: Session = Depends(get_db)):
    data = product_service.get_products(db)
    return ApiResponse(data=data)

@router.get("/products/summary", response_model=ApiResponse)
def product_summary(db: Session = Depends(get_db)):
    data = product_service.get_product_summary(db)
    return ApiResponse(data=data)

@router.get("/products/{product_id}", response_model=ApiResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    data = product_service.get_product(db, product_id)
    if not data:
        return ApiResponse(code=404, message="商品不存在")
    return ApiResponse(data=data)

@router.post("/products", response_model=ApiResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    product = product_service.create_product(db, data)
    return ApiResponse(data=ProductResponse.model_validate(product))

@router.put("/products/{product_id}", response_model=ApiResponse)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = product_service.update_product(db, product_id, data)
    if not product:
        return ApiResponse(code=404, message="商品不存在")
    return ApiResponse(data=ProductResponse.model_validate(product))

@router.delete("/products/{product_id}", response_model=ApiResponse)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = product_service.delete_product(db, product_id)
    if not ok:
        return ApiResponse(code=404, message="商品不存在")
    return ApiResponse(message="删除成功")

@router.post("/products/{product_id}/sell", response_model=ApiResponse)
def sell_product(product_id: int, data: SellRequest, db: Session = Depends(get_db)):
    result = product_service.sell_product(db, product_id, data.quantity)
    if result is None:
        return ApiResponse(code=404, message="商品不存在")
    if isinstance(result, dict) and "error" in result:
        return ApiResponse(code=400, message=result["error"])
    return ApiResponse(data=ProductResponse.model_validate(result))
