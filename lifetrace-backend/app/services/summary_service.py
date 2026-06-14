from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.stall_log import StallLog
from app.models.weather import Weather
from app.models.schedule import Schedule
from app.models.product import Product
from app.models.queue_order import QueueOrder

def get_today_summary(db: Session):
    today = date.today()

    stalls = db.query(StallLog).filter(StallLog.date == today).all()
    stall_count = len(stalls)
    stall_income = sum(s.income for s in stalls)
    stall_profit = sum(s.profit for s in stalls)

    weather = db.query(Weather).filter(Weather.date == today).first()

    schedules = db.query(Schedule).filter(Schedule.date == today).all()
    unfinished = [s for s in schedules if s.status != "已完成"]
    unfinished_count = len(unfinished)

    products = db.query(Product).all()
    product_count = len(products)
    low_stock_count = sum(1 for p in products if 0 < p.stock < 10)
    sold_out_count = sum(1 for p in products if p.stock == 0)

    queue_waiting = db.query(QueueOrder).filter(QueueOrder.status == "等待中").count()
    queue_serving = db.query(QueueOrder).filter(QueueOrder.status == "服务中").count()
    queue_total = queue_waiting + queue_serving

    advice_items = []
    if stall_count == 0:
        advice_items.append("今日暂无出摊记录")
    if unfinished_count > 5:
        advice_items.append(f"未完成事项较多（{unfinished_count}项），注意时间安排")
    if low_stock_count > 0:
        advice_items.append(f"{low_stock_count}种商品库存不足，建议及时补货")
    if sold_out_count > 0:
        advice_items.append(f"{sold_out_count}种商品已售空")
    if queue_total > 5:
        advice_items.append("排队人数较多，建议加快服务速度")

    return {
        "date": today.isoformat(),
        "stall": {
            "count": stall_count,
            "total_income": round(stall_income, 2),
            "total_profit": round(stall_profit, 2),
        },
        "weather": {
            "has_data": weather is not None,
            "temperature": weather.temperature if weather else None,
            "weather_type": weather.weather_type if weather else None,
            "is_rainy": weather.is_rainy if weather else None,
            "wind_level": weather.wind_level if weather else None,
        } if weather else {"has_data": False},
        "schedule": {
            "unfinished_count": unfinished_count,
            "total_count": len(schedules),
        },
        "product": {
            "total_count": product_count,
            "low_stock_count": low_stock_count,
            "sold_out_count": sold_out_count,
        },
        "queue": {
            "waiting_count": queue_waiting,
            "serving_count": queue_serving,
            "total_count": queue_total,
        },
        "advice": advice_items,
    }
