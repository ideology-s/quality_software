from datetime import date
from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate

def get_schedules(db: Session):
    return db.query(Schedule).order_by(Schedule.date, Schedule.start).all()

def get_schedules_by_date(db: Session, target_date: date):
    return db.query(Schedule).filter(Schedule.date == target_date).order_by(Schedule.start).all()

def get_schedule(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()

def create_schedule(db: Session, data: ScheduleCreate):
    item = Schedule(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def update_schedule(db: Session, schedule_id: int, data: ScheduleUpdate):
    item = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not item:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    db.commit()
    db.refresh(item)
    return item

def delete_schedule(db: Session, schedule_id: int):
    item = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

def get_schedule_summary(db: Session):
    all_items = db.query(Schedule).all()
    total = len(all_items)
    completed = sum(1 for s in all_items if s.status == "已完成")
    pending = total - completed
    return {
        "pending_count": pending,
        "completed_count": completed,
        "total_count": total,
    }
