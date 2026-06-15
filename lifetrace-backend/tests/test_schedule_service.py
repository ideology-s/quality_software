"""
白盒测试 —— schedule_service（日程清单管理）

覆盖范围：
- CRUD 正常/异常路径（不存在 ID 的查询/更新/删除）
- get_schedule_summary() 汇总统计
- 边界值：空列表、所有完成、所有未完成
"""
from datetime import date
from unittest.mock import MagicMock

from app.services import schedule_service
from app.models.schedule import Schedule


def _schedule(**kw):
    s = MagicMock(spec=Schedule)
    s.id = kw.get("id", 1)
    s.date = kw.get("date", date(2026, 6, 15))
    s.start = kw.get("start", "09:00")
    s.end = kw.get("end", "10:30")
    s.task = kw.get("task", "进货采购")
    s.status = kw.get("status", "待办")
    return s


class TestGetScheduleSummary:
    """日程汇总统计 —— 4 个等价路径"""

    def test_empty(self, db):
        """无日程 → 全部为 0"""
        db.query().all.return_value = []
        result = schedule_service.get_schedule_summary(db)
        assert result == {"pending_count": 0, "completed_count": 0, "total_count": 0}

    def test_all_pending(self, db):
        """3 条待办，0 完成"""
        items = [
            _schedule(id=1, status="待办"),
            _schedule(id=2, status="未开始"),
            _schedule(id=3, status="进行中"),
        ]
        db.query().all.return_value = items
        result = schedule_service.get_schedule_summary(db)
        assert result["pending_count"] == 3
        assert result["completed_count"] == 0
        assert result["total_count"] == 3

    def test_all_completed(self, db):
        """全部已完成"""
        items = [_schedule(id=1, status="已完成"), _schedule(id=2, status="已完成")]
        db.query().all.return_value = items
        result = schedule_service.get_schedule_summary(db)
        assert result["pending_count"] == 0
        assert result["completed_count"] == 2

    def test_mixed(self, db):
        """混合状态"""
        items = [
            _schedule(id=1, status="已完成"),
            _schedule(id=2, status="待办"),
            _schedule(id=3, status="已完成"),
            _schedule(id=4, status="进行中"),
            _schedule(id=5, status="未开始"),
        ]
        db.query().all.return_value = items
        result = schedule_service.get_schedule_summary(db)
        assert result["pending_count"] == 3
        assert result["completed_count"] == 2
        assert result["total_count"] == 5


class TestScheduleCRUD:
    def test_get_schedule_found(self, db):
        s = _schedule(id=1)
        db.query().filter().first.return_value = s
        result = schedule_service.get_schedule(db, 1)
        assert result is s

    def test_get_schedule_not_found(self, db):
        db.query().filter().first.return_value = None
        result = schedule_service.get_schedule(db, 999)
        assert result is None

    def test_update_not_found(self, db):
        db.query().filter().first.return_value = None
        result = schedule_service.update_schedule(db, 999, MagicMock())
        assert result is None

    def test_delete_not_found(self, db):
        db.query().filter().first.return_value = None
        result = schedule_service.delete_schedule(db, 999)
        assert result is False

    def test_delete_success(self, db):
        s = _schedule(id=1)
        db.query().filter().first.return_value = s
        result = schedule_service.delete_schedule(db, 1)
        assert result is True
        db.delete.assert_called_once_with(s)
        db.commit.assert_called()
