from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.stall_log import StallLog
from app.models.weather import Weather
from app.schemas.stall_log import StallLogCreate, StallLogUpdate, WeatherCreate

def get_stall_logs(db: Session):
    return db.query(StallLog).order_by(StallLog.date.desc(), StallLog.start_time.desc()).all()

def get_stall_log(db: Session, log_id: int):
    return db.query(StallLog).filter(StallLog.id == log_id).first()

def create_stall_log(db: Session, data: StallLogCreate):
    log = StallLog(**data.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def update_stall_log(db: Session, log_id: int, data: StallLogUpdate):
    log = db.query(StallLog).filter(StallLog.id == log_id).first()
    if not log:
        return None
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(log, key, val)
    db.commit()
    db.refresh(log)
    return log

def delete_stall_log(db: Session, log_id: int):
    log = db.query(StallLog).filter(StallLog.id == log_id).first()
    if not log:
        return False
    db.delete(log)
    db.commit()
    return True

def get_weekly_summary(db: Session):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    logs = db.query(StallLog).filter(StallLog.date >= week_start).all()
    count = len(logs)
    total_hours = 0.0
    total_income = 0.0
    total_profit = 0.0
    for log in logs:
        start = log.start_time
        end = log.end_time
        hours = (end.hour * 60 + end.minute - start.hour * 60 - start.minute) / 60
        total_hours += max(hours, 0)
        total_income += log.income
        total_profit += log.profit
    return {
        "count": count,
        "total_hours": round(total_hours, 1),
        "total_income": round(total_income, 2),
        "total_profit": round(total_profit, 2),
    }

def set_weather(db: Session, data: WeatherCreate):
    today = date.today()
    existing = db.query(Weather).filter(Weather.date == today).first()
    if existing:
        for key, val in data.model_dump().items():
            setattr(existing, key, val)
        db.commit()
        db.refresh(existing)
        return existing
    record = Weather(date=today, **data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_today_weather(db: Session):
    return db.query(Weather).filter(Weather.date == date.today()).first()

def get_stall_advice(db: Session, sleep_hours: float, work_hours: float,
                     is_unwell: bool, planned_stall_hours: float, location_type: str):
    details = []
    health_status = "normal"
    fatigue_status = "normal"
    is_recommended = True

    if sleep_hours < 6:
        details.append("睡眠不足，建议今晚早睡")
        health_status = "warning"
        is_recommended = False
    else:
        details.append("睡眠充足")

    if work_hours > 8:
        details.append("昨日工作时长较长，可能存在疲劳风险")
        fatigue_status = "warning"
        is_recommended = False
    else:
        details.append("工作强度正常")

    if is_unwell:
        details.append("身体不适，不建议长时间出摊")
        health_status = "warning"
        is_recommended = False

    if planned_stall_hours > 4:
        details.append("计划出摊时间较长，注意体力消耗")

    weather = get_today_weather(db)
    weather_status = "normal"
    if weather:
        if weather.temperature > 35:
            details.append(f"温度 {weather.temperature}℃，天气炎热，不建议长时间户外出摊")
            weather_status = "warning"
            is_recommended = False
        elif weather.temperature < 5:
            details.append(f"温度 {weather.temperature}℃，天气寒冷，注意保暖")
            weather_status = "warning"
            is_recommended = False
        else:
            details.append("天气温度适宜")

        if weather.is_rainy:
            details.append("当日降雨，准备遮雨工具，注意商品防潮")
            weather_status = "warning"
            is_recommended = False

        if weather.wind_level >= 5:
            details.append(f"风力 {weather.wind_level}级，不适合摆放轻便商品或进行户外出摊")
            weather_status = "warning"
            is_recommended = False

        if weather.is_rainy and location_type == "室外":
            details.append("天气恶劣且出摊地点为室外，建议取消或改为室内经营")
            is_recommended = False
    else:
        details.append("暂无天气数据，建议手动填写天气信息")

    if is_unwell and weather and (weather.is_rainy or weather.wind_level >= 5):
        details.append("身体不适且天气恶劣，强烈建议不出摊")
        is_recommended = False

    if health_status == "normal" and weather_status == "normal" and fatigue_status == "normal":
        overall_advice = "身体状况良好，天气条件适宜，适合正常出摊"
    elif health_status == "warning" and weather_status == "warning":
        overall_advice = "健康状态和天气条件均不理想，建议调整出摊计划"
    elif health_status == "warning":
        overall_advice = "身体健康状况一般，建议适当调整出摊安排"
    elif weather_status == "warning":
        overall_advice = "天气条件不太理想，建议做好防护准备"
    else:
        overall_advice = "条件基本正常，注意合理安排"

    return {
        "health_status": health_status,
        "weather_status": weather_status,
        "fatigue_status": fatigue_status,
        "overall_advice": overall_advice,
        "details": details,
        "is_recommended": is_recommended,
    }
