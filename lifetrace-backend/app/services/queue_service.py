import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.queue_order import QueueOrder
from app.models.product import Product
from app.models.stall_log import StallLog
from app.schemas.queue_order import QueueOrderCreate

def take_number(db: Session, data: QueueOrderCreate):
    active_stall = db.query(StallLog).filter(StallLog.status == "进行中").first()
    if not active_stall:
        return {"error": "当前未出摊，请先开始出摊再取号"}

    existing = db.query(QueueOrder).filter(
        QueueOrder.customer == data.customer,
        QueueOrder.status.in_(["等待中", "服务中"])
    ).first()
    if existing:
        return {"error": f"顾客 {data.customer} 已有未完成订单，不能重复取号"}

    items_data = []
    total_price = 0.0
    total_cost = 0.0
    order_parts = []

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            return {"error": f"商品不存在 (id={item.product_id})"}
        if item.quantity <= 0:
            return {"error": f"商品 {product.name} 数量必须大于 0"}
        if item.quantity > product.stock:
            return {"error": f"商品 {product.name} 库存不足，当前库存 {product.stock}，请求 {item.quantity}"}

        item_price = product.price * item.quantity
        item_cost = product.cost * item.quantity
        total_price += item_price
        total_cost += item_cost

        product.stock -= item.quantity
        product.sold += item.quantity

        items_data.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "cost": product.cost,
            "quantity": item.quantity,
        })
        order_parts.append(f"{product.name}×{item.quantity}")

    max_num = db.query(func.max(QueueOrder.id)).scalar() or 0
    next_num = max_num + 1
    number = f"A{next_num:03d}"

    has_serving = db.query(QueueOrder).filter(QueueOrder.status == "服务中").first()
    status = "等待中" if has_serving else "服务中"

    order = QueueOrder(
        number=number,
        customer=data.customer,
        order_content=", ".join(order_parts),
        quantity=f"×{sum(i.quantity for i in data.items)}",
        note=data.note or "无备注",
        status=status,
        items=items_data,
        total_price=round(total_price, 2),
        total_cost=round(total_cost, 2),
        stall_log_id=active_stall.id if active_stall else None,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_queue_list(db: Session):
    orders = db.query(QueueOrder).filter(
        QueueOrder.status.in_(["等待中", "服务中"])
    ).order_by(QueueOrder.id).all()
    return _format_orders(orders)

def get_all_orders(db: Session):
    orders = db.query(QueueOrder).order_by(QueueOrder.id).all()
    return _format_orders(orders)

def get_queue_summary(db: Session):
    waiting = db.query(QueueOrder).filter(QueueOrder.status == "等待中").count()
    serving = db.query(QueueOrder).filter(QueueOrder.status == "服务中").first()
    total = waiting + (1 if serving else 0)
    max_id = db.query(func.max(QueueOrder.id)).scalar() or 0
    next_number = f"A{max_id + 1:03d}"
    return {
        "current_number": serving.number if serving else None,
        "queue_count": total,
        "is_crowded": total > 5,
        "next_number": next_number,
    }

def serve_next(db: Session):
    serving = db.query(QueueOrder).filter(QueueOrder.status == "服务中").first()
    if serving:
        return {"error": "当前已有顾客正在服务中，请先完成或取消当前订单"}

    next_order = db.query(QueueOrder).filter(
        QueueOrder.status == "等待中"
    ).order_by(QueueOrder.id).first()

    if not next_order:
        return {"error": "当前队列为空，暂无顾客排队"}

    next_order.status = "服务中"
    db.commit()
    db.refresh(next_order)
    return next_order

def complete_order(db: Session, number: str):
    order = db.query(QueueOrder).filter(QueueOrder.number == number).first()
    if not order:
        return None
    order.status = "已完成"
    db.commit()
    db.refresh(order)
    return order

def cancel_order(db: Session, number: str):
    order = db.query(QueueOrder).filter(QueueOrder.number == number).first()
    if not order:
        return None
    order.status = "已取消"
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, number: str):
    order = db.query(QueueOrder).filter(QueueOrder.number == number).first()
    if not order:
        return False
    db.delete(order)
    db.commit()
    return True

def _format_orders(orders):
    result = []
    for o in orders:
        items_list = o.items if isinstance(o.items, list) else (json.loads(o.items) if o.items else [])

        result.append({
            "number": o.number,
            "customer": o.customer,
            "order": o.order_content,
            "quantity": o.quantity,
            "note": o.note or "无备注",
            "status": o.status,
            "items": items_list,
            "total_price": o.total_price or 0,
            "total_cost": o.total_cost or 0,
            "stall_log_id": o.stall_log_id,
        })
    return result
