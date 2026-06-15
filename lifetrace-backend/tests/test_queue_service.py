"""
白盒测试 —— queue_service（排队取号与订单服务）

覆盖范围：
- take_number()：正常取号、重复取号、空队列首个自动服务中
- serve_next()：正常叫号、已有服务中、空队列
- complete_order() / cancel_order()：正常、不存在
- get_queue_summary()：人数统计、拥挤判断
- 状态流转：等待中 → 服务中 → 已完成/已取消
"""
from unittest.mock import MagicMock

import pytest

from app.services import queue_service
from app.models.queue_order import QueueOrder


def _order(**kw):
    o = MagicMock(spec=QueueOrder)
    o.id = kw.get("id", 1)
    o.number = kw.get("number", "A001")
    o.customer = kw.get("customer", "测试顾客")
    o.order_content = kw.get("order_content", "烤串")
    o.quantity = kw.get("quantity", "×1")
    o.note = kw.get("note", "无备注")
    o.status = kw.get("status", "等待中")
    return o


# ─── take_number ──────────────────────────────────────────────

class TestTakeNumber:
    def test_first_customer_serving(self, db):
        """第一个顾客 → 直接进入服务中"""
        db.query().filter().first.return_value = None  # no existing
        db.query().scalar.return_value = 0  # max id

        result = queue_service.take_number(
            db,
            data=MagicMock(customer="张三", order="烤串", quantity="×2", note="多辣"),
        )

        assert result.status == "服务中"

    def test_second_customer_waiting(self, db):
        """第二个顾客 → 等待中"""
        # first call: no duplicate check
        db.query().filter().first.side_effect = [
            None,  # duplicate check
            _order(status="服务中"),  # has_serving check
        ]
        db.query().scalar.return_value = 1

        result = queue_service.take_number(
            db,
            data=MagicMock(customer="李四", order="零食包", quantity="×1", note=""),
        )

        assert result.status == "等待中"

    def test_duplicate_customer(self, db):
        """同一顾客有未完成订单 → 返回 error"""
        existing = _order(customer="张三", status="等待中")
        db.query().filter().first.return_value = existing

        result = queue_service.take_number(
            db,
            data=MagicMock(customer="张三", order="烤串", quantity="×1", note=""),
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "已有未完成" in result["error"] or "不能重复" in result["error"]


# ─── serve_next ───────────────────────────────────────────────

class TestServeNext:
    def test_serve_next_success(self, db):
        """正常叫号：下一个等待中 → 服务中"""
        serving = None
        waiting = _order(id=2, number="A002", status="等待中")

        db.query().filter().first.side_effect = [serving, waiting]  # serving check, next
        # .filter().order_by().first() for next_order

        result = queue_service.serve_next(db)

        assert result is waiting
        assert waiting.status == "服务中"

    def test_serve_next_already_serving(self, db):
        """已有服务中的顾客 → 返回 error"""
        db.query().filter().first.return_value = _order(status="服务中")

        result = queue_service.serve_next(db)
        assert isinstance(result, dict)
        assert "error" in result

    def test_serve_next_empty_queue(self, db):
        """队列为空 → 返回 error"""
        db.query().filter().first.side_effect = [None, None]

        result = queue_service.serve_next(db)
        assert isinstance(result, dict)
        assert "队列为空" in result["error"] or "暂无顾客" in result["error"]


# ─── complete / cancel ────────────────────────────────────────

class TestCompleteCancel:
    def test_complete_order_success(self, db):
        o = _order(number="A001", status="服务中")
        db.query().filter().first.return_value = o

        result = queue_service.complete_order(db, "A001")
        assert result is o
        assert o.status == "已完成"

    def test_complete_order_not_found(self, db):
        db.query().filter().first.return_value = None
        result = queue_service.complete_order(db, "A999")
        assert result is None

    def test_cancel_order_success(self, db):
        o = _order(number="A001", status="服务中")
        db.query().filter().first.return_value = o

        result = queue_service.cancel_order(db, "A001")
        assert result is o
        assert o.status == "已取消"

    def test_cancel_order_not_found(self, db):
        db.query().filter().first.return_value = None
        result = queue_service.cancel_order(db, "A999")
        assert result is None


# ─── get_queue_summary ────────────────────────────────────────

class TestQueueSummary:
    def test_empty(self, db):
        """队列为空 → count=0, current_number=None"""
        db.query().filter().count.return_value = 0
        db.query().filter().first.return_value = None

        result = queue_service.get_queue_summary(db)
        assert result["queue_count"] == 0
        assert result["current_number"] is None
        assert result["is_crowded"] is False

    def test_crowded(self, db):
        """6 人等待 → is_crowded=True"""
        db.query().filter().count.return_value = 6
        db.query().filter().first.return_value = _order(number="A001", status="服务中")

        result = queue_service.get_queue_summary(db)
        assert result["queue_count"] == 7  # 6 waiting + 1 serving
        assert result["is_crowded"] is True

    def test_not_crowded(self, db):
        """3 人等待 → is_crowded=False"""
        db.query().filter().count.return_value = 3
        db.query().filter().first.return_value = _order(number="A001", status="服务中")

        result = queue_service.get_queue_summary(db)
        assert result["queue_count"] == 4
        assert result["is_crowded"] is False


# ─── delete ───────────────────────────────────────────────────

class TestDeleteOrder:
    def test_delete_success(self, db):
        o = _order(number="A001")
        db.query().filter().first.return_value = o
        result = queue_service.delete_order(db, "A001")
        assert result is True
        db.delete.assert_called_once_with(o)

    def test_delete_not_found(self, db):
        db.query().filter().first.return_value = None
        result = queue_service.delete_order(db, "A999")
        assert result is False
