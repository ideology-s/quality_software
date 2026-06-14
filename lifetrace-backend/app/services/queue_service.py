from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.queue_order import QueueOrder
from app.schemas.queue_order import QueueOrderCreate

def take_number(db: Session, data: QueueOrderCreate):
    existing = db.query(QueueOrder).filter(
        QueueOrder.customer == data.customer,
        QueueOrder.status.in_(["等待中", "服务中"])
    ).first()
    if existing:
        return {"error": f"顾客 {data.customer} 已有未完成订单，不能重复取号"}

    max_num = db.query(func.max(QueueOrder.id)).scalar() or 0
    next_num = max_num + 1
    number = f"A{next_num:03d}"

    has_serving = db.query(QueueOrder).filter(QueueOrder.status == "服务中").first()
    status = "等待中" if has_serving else "服务中"

    order = QueueOrder(
        number=number,
        customer=data.customer,
        order_content=data.order,
        quantity=data.quantity,
        note=data.note or "无备注",
        status=status,
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
    return {
        "current_number": serving.number if serving else None,
        "queue_count": total,
        "is_crowded": total > 5,
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
        result.append({
            "number": o.number,
            "customer": o.customer,
            "order": o.order_content,
            "quantity": o.quantity,
            "note": o.note or "无备注",
            "status": o.status,
        })
    return result
