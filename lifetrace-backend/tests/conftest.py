"""
测试公共 fixtures —— mock SQLAlchemy Session，用于白盒单元测试。
"""
import pytest
from unittest.mock import MagicMock


def make_mock_query(items=None, first_item=None, scalar_value=None):
    """构建可无限链式调用的 mock query。"""
    q = MagicMock()
    items = items or []

    q.all.return_value = items
    q.first.return_value = first_item if first_item is not None else (items[0] if items else None)
    q.scalar.return_value = scalar_value
    q.count.return_value = len(items)

    # 链式调用：.filter()/.order_by() 均返回自身
    q.filter.return_value = q
    q.order_by.return_value = q
    # .in_() 是 list 操作，返回自身即可
    q.in_.return_value = q

    return q


@pytest.fixture
def db():
    """返回 mock SQLAlchemy Session，db.query(Model) 返回统一的可链式 mock query。"""
    session = MagicMock()
    default_q = make_mock_query()
    session.query.return_value = default_q
    return session
