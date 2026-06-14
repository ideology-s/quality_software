from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_products(db: Session):
    products = db.query(Product).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "cost": p.cost,
            "stock": p.stock,
            "sold": p.sold,
            "image": p.image or "",
            "stock_status": _get_stock_status(p.stock),
        })
    return result

def get_product(db: Session, product_id: int):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        return None
    income = p.price * p.sold
    profit = max(p.price - p.cost, 0) * p.sold
    return {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "cost": p.cost,
        "stock": p.stock,
        "sold": p.sold,
        "image": p.image or "",
        "income": round(income, 2),
        "profit": round(profit, 2),
        "stock_status": _get_stock_status(p.stock),
        "is_loss_sale": p.price < p.cost,
    }

def create_product(db: Session, data: ProductCreate):
    p = Product(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def update_product(db: Session, product_id: int, data: ProductUpdate):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(p, key, val)
    db.commit()
    db.refresh(p)
    return p

def delete_product(db: Session, product_id: int):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True

def sell_product(db: Session, product_id: int, quantity: int):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        return None
    if quantity > p.stock:
        return {"error": f"库存不足，当前库存 {p.stock}，请求售卖 {quantity}"}
    p.stock -= quantity
    p.sold += quantity
    db.commit()
    db.refresh(p)
    return p

def get_product_summary(db: Session):
    products = db.query(Product).all()
    total_income = sum(p.price * p.sold for p in products)
    total_profit = sum(max(p.price - p.cost, 0) * p.sold for p in products)
    return {
        "total_income": round(total_income, 2),
        "total_profit": round(total_profit, 2),
        "product_count": len(products),
    }

def _get_stock_status(stock: int):
    if stock == 0:
        return "sold_out"
    elif stock < 10:
        return "insufficient"
    return "normal"
