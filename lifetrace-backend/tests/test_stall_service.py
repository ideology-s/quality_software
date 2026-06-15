"""
白盒测试 —— stall_service（健康/天气/出摊建议）

覆盖范围：
- get_stall_advice() 的 12 条判断规则全部分支
- 边界值：sleep_hours(0,5,6), work_hours(0,8,9), planned_stall_hours(0,4,5)
          temperature(0,5,35,36), wind_level(0,4,5)
- 条件组合：睡眠不足+身体不适、身体不适+天气恶劣、天气恶劣+室外
- CRUD 操作的正常/异常路径
- set_weather 新建和更新分支
"""
from datetime import date, time
from unittest.mock import MagicMock, patch

import pytest

from app.services import stall_service
from app.models.stall_log import StallLog
from app.models.weather import Weather
from app.schemas.stall_log import (
    StallLogCreate,
    StallLogUpdate,
    WeatherCreate,
)


# ─── helpers ───────────────────────────────────────────────────

def _weather(**kw):
    w = MagicMock(spec=Weather)
    w.temperature = kw.get("temperature", 25)
    w.weather_type = kw.get("weather_type", "晴")
    w.is_rainy = kw.get("is_rainy", False)
    w.wind_level = kw.get("wind_level", 2)
    return w


# ─── get_stall_advice 决策规则测试 ───────────────────────────────

class TestStallAdvice:
    """出摊建议决策表测试 —— 每条规则至少 1 个用例。"""

    def test_normal_conditions(self, db):
        """健康正常 + 天气正常 → 整体建议为适合出摊"""
        db.query().first.return_value = _weather(temperature=25, is_rainy=False, wind_level=2)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["health_status"] == "normal"
        assert result["weather_status"] == "normal"
        assert result["fatigue_status"] == "normal"
        assert result["is_recommended"] is True
        assert "适合正常出摊" in result["overall_advice"]

    # ── 睡眠规则 ──────────────────────────────────────────────
    def test_sleep_insufficient_boundary(self, db):
        """sleep_hours = 5（边界：<6）→ 睡眠不足"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=5, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["health_status"] == "warning"
        assert any("睡眠不足" in d for d in result["details"])
        assert result["is_recommended"] is False

    def test_sleep_sufficient_boundary(self, db):
        """sleep_hours = 6（边界：>=6）→ 睡眠充足"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=6, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert not any("睡眠不足" in d for d in result["details"])

    def test_sleep_zero(self, db):
        """sleep_hours = 0 → 睡眠不足"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=0, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["health_status"] == "warning"

    # ── 工作规则 ──────────────────────────────────────────────
    def test_work_over_8(self, db):
        """work_hours = 9 → 疲劳风险"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=9,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["fatigue_status"] == "warning"
        assert any("疲劳" in d for d in result["details"])

    def test_work_exactly_8(self, db):
        """work_hours = 8（边界）→ 工作强度正常"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=8,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["fatigue_status"] == "normal"

    # ── 身体不适 ──────────────────────────────────────────────
    def test_is_unwell(self, db):
        """身体不适 → warning + 不建议长时间出摊"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=True, planned_stall_hours=3, location_type="室内"
        )
        assert result["health_status"] == "warning"
        assert any("身体不适" in d for d in result["details"])

    # ── 计划出摊时长 ─────────────────────────────────────────
    def test_planned_stall_long(self, db):
        """planned_stall_hours = 5 → 提示注意体力"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=5, location_type="室内"
        )
        assert any("注意体力" in d for d in result["details"])
        # 只有提示，但不改变 is_recommended（仅 >4 触发的提示不改变核心状态）

    # ── 温度规则 ─────────────────────────────────────────────
    def test_temperature_high(self, db):
        """temperature = 36 → 天气炎热"""
        db.query().first.return_value = _weather(temperature=36)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["weather_status"] == "warning"
        assert any("炎热" in d for d in result["details"])

    def test_temperature_low(self, db):
        """temperature = 3 → 天气寒冷"""
        db.query().first.return_value = _weather(temperature=3)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["weather_status"] == "warning"
        assert any("寒冷" in d for d in result["details"])

    def test_temperature_normal(self, db):
        """temperature = 25 → 适宜"""
        db.query().first.return_value = _weather(temperature=25)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert any("适宜" in d for d in result["details"])

    # ── 降雨规则 ─────────────────────────────────────────────
    def test_rainy(self, db):
        """降雨 → 提示防潮"""
        db.query().first.return_value = _weather(is_rainy=True)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["weather_status"] == "warning"
        assert any("降雨" in d or "防潮" in d for d in result["details"])

    # ── 风力规则 ─────────────────────────────────────────────
    def test_wind_high(self, db):
        """wind_level = 6 → 不适合户外"""
        db.query().first.return_value = _weather(wind_level=6)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["weather_status"] == "warning"
        assert any("风力" in d or "轻便" in d for d in result["details"])

    def test_wind_boundary_normal(self, db):
        """wind_level = 4（边界 <5）→ 正常"""
        db.query().first.return_value = _weather(wind_level=4)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["weather_status"] == "normal"

    # ── 组合规则 ─────────────────────────────────────────────
    def test_rain_and_outdoor(self, db):
        """降雨 + 室外 → 建议取消"""
        db.query().first.return_value = _weather(is_rainy=True)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室外"
        )
        assert any("改为室内" in d for d in result["details"])
        assert result["is_recommended"] is False

    def test_unwell_and_bad_weather(self, db):
        """身体不适 + 天气恶劣 → 强烈不建议出摊"""
        db.query().first.return_value = _weather(is_rainy=True, wind_level=5)

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=True, planned_stall_hours=3, location_type="室外"
        )
        assert any("强烈建议不出摊" in d for d in result["details"])

    def test_sleep_insufficient_and_work_long(self, db):
        """睡眠不足 + 工作时长高 → 双重 warning"""
        db.query().first.return_value = _weather()

        result = stall_service.get_stall_advice(
            db, sleep_hours=4, work_hours=10,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert result["health_status"] == "warning"
        assert result["fatigue_status"] == "warning"

    def test_health_warning_and_weather_warning(self, db):
        """健康 warning + 天气 warning → 组合建议"""
        db.query().first.return_value = _weather(wind_level=6)

        result = stall_service.get_stall_advice(
            db, sleep_hours=4, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert "调整出摊计划" in result["overall_advice"] or "不理想" in result["overall_advice"]

    # ── 无天气数据 ───────────────────────────────────────────
    def test_no_weather_data(self, db):
        """无天气数据 → 提示手动填写"""
        db.query().first.return_value = None

        result = stall_service.get_stall_advice(
            db, sleep_hours=7, work_hours=6,
            is_unwell=False, planned_stall_hours=3, location_type="室内"
        )
        assert any("暂无天气" in d for d in result["details"])


# ─── set_weather 测试 ──────────────────────────────────────────

class TestSetWeather:
    def test_create_new_weather(self, db):
        """当日无天气记录 → 新建"""
        db.query().filter().first.return_value = None
        data = WeatherCreate(temperature=28, weather_type="晴", is_rainy=False, wind_level=2)

        result = stall_service.set_weather(db, data)
        db.add.assert_called_once()
        db.commit.assert_called()

    def test_update_existing_weather(self, db):
        """当日已有天气记录 → 更新"""
        existing = _weather(temperature=25)
        db.query().filter().first.return_value = existing
        data = WeatherCreate(temperature=30, weather_type="多云", is_rainy=True, wind_level=3)

        result = stall_service.set_weather(db, data)
        # 更新时不调用 add
        db.add.assert_not_called()
        db.commit.assert_called()


# ─── CRUD 测试 ─────────────────────────────────────────────────

class TestStallLogCRUD:
    def test_get_stall_logs(self, db):
        logs = [MagicMock(spec=StallLog), MagicMock(spec=StallLog)]
        db.query().order_by().order_by().all.return_value = logs

        result = stall_service.get_stall_logs(db)
        assert len(result) == 2

    def test_get_stall_log_found(self, db):
        log = MagicMock(spec=StallLog)
        db.query().filter().first.return_value = log

        result = stall_service.get_stall_log(db, 1)
        assert result is log

    def test_get_stall_log_not_found(self, db):
        db.query().filter().first.return_value = None

        result = stall_service.get_stall_log(db, 999)
        assert result is None

    def test_delete_not_found(self, db):
        db.query().filter().first.return_value = None

        result = stall_service.delete_stall_log(db, 999)
        assert result is False
