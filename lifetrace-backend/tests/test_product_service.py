"""
白盒测试 —— product_service（商品管理/售卖/库存状态）

覆盖范围：
- _get_stock_status() 三种分支：sold_out / insufficient / normal
- sell_product() 正常售卖、库存不足、商品不存在
- get_product() 详情（收入/利润/亏本判断）
- get_product_summary() 汇总计算
- CRUD 边界：不存在 ID 的返回
"""
from unittest.mock import MagicMock

import pytest

from app.services import product_service
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


# ─── helpers ───────────────────────────────────────────────────

def _product(**kw):
    p = MagicMock(spec=Product)
    p.id = kw.get("id", 1)
    p.name = kw.get("name", "测试商品")
    p.price = kw.get("price", 15.0)
    p.cost = kw.get("cost", 10.0)
    p.stock = kw.get("stock", 20)
    p.sold = kw.get("sold", 0)
    p.image = kw.get("image", "")
    return p


# ─── _get_stock_status 单元测试 ────────────────────────────────

class TestStockStatus:
    """库存状态判断 —— 3 个等价类"""

    def test_sold_out(self):
        """stock = 0 → sold_out"""
        assert product_service._get_stock_status(0) == "sold_out"

    def test_insufficient_low(self):
        """stock = 1（边界）→ insufficient"""
        assert product_service._get_stock_status(1) == "insufficient"

    def test_insufficient_high(self):
        """stock = 9（边界）→ insufficient"""
        assert product_service._get_stock_status(9) == "insufficient"

    def test_normal_low(self):
        """stock = 10（边界）→ normal"""
        assert product_service._get_stock_status(10) == "normal"

    def test_normal_high(self):
        """stock = 999 → normal"""
        assert product_service._get_stock_status(999) == "normal"


# ─── sell_product 测试 ────────────────────────────────────────

class TestSellProduct:
    def test_sell_success(self, db):
        """正常售卖：库存减少，已售增加"""
        p = _product(stock=10, sold=2)
        db.query().filter().first.return_value = p

        result = product_service.sell_product(db, 1, quantity=3)

        assert result is p
        assert p.stock == 7  # 10 - 3
        assert p.sold == 5  # 2 + 3
        db.commit.assert_called()

    def test_sell_insufficient_stock(self, db):
        """售卖数量 > 库存 → 返回 error dict"""
        p = _product(stock=3, sold=0)
        db.query().filter().first.return_value = p

        result = product_service.sell_product(db, 1, quantity=5)

        assert isinstance(result, dict)
        assert "error" in result
        assert "库存不足" in result["error"]
        # 库存不应被修改
        assert p.stock == 3

    def test_sell_exactly_all(self, db):
        """售卖数量恰好等于库存 → stock 归零"""
        p = _product(stock=5, sold=0)
        db.query().filter().first.return_value = p

        result = product_service.sell_product(db, 1, quantity=5)
        assert result is p
        assert p.stock == 0
        assert p.sold == 5

    def test_sell_product_not_found(self, db):
        """售卖不存在的商品 → 返回 None"""
        db.query().filter().first.return_value = None

        result = product_service.sell_product(db, 999, quantity=1)
        assert result is None


# ─── get_product 测试 ─────────────────────────────────────────

class TestGetProduct:
    def test_detail_with_profit(self, db):
        """price=15, cost=10, sold=5 → income=75, profit=25"""
        p = _product(price=15, cost=10, stock=20, sold=5)
        db.query().filter().first.return_value = p

        result = product_service.get_product(db, 1)

        assert result["income"] == 75.0
        assert result["profit"] == 25.0
        assert result["is_loss_sale"] is False

    def test_detail_loss_sale(self, db):
        """price=8 < cost=12 → 亏本销售"""
        p = _product(price=8, cost=12, stock=10, sold=3)
        db.query().filter().first.return_value = p

        result = product_service.get_product(db, 1)

        assert result["is_loss_sale"] is True
        # 利润不应该为负（已做 max 保护）
        assert result["profit"] == 0.0

    def test_detail_not_found(self, db):
        db.query().filter().first.return_value = None
        result = product_service.get_product(db, 999)
        assert result is None


# ─── get_product_summary 测试 ─────────────────────────────────

class TestProductSummary:
    def test_summary_empty(self, db):
        db.query().all.return_value = []
        result = product_service.get_product_summary(db)
        assert result["total_income"] == 0
        assert result["total_profit"] == 0
        assert result["product_count"] == 0

    def test_summary_multi_products(self, db):
        p1 = _product(id=1, price=10, cost=5, sold=3)   # income=30, profit=15
        p2 = _product(id=2, price=8, cost=12, sold=2)     # income=16, profit=0 (亏本)
        db.query().all.return_value = [p1, p2]

        result = product_service.get_product_summary(db)
        assert result["total_income"] == 46.0
        assert result["total_profit"] == 15.0
        assert result["product_count"] == 2


# ─── CRUD 测试 ────────────────────────────────────────────────

class TestProductCRUD:
    def test_get_products_empty(self, db):
        db.query().all.return_value = []
        result = product_service.get_products(db)
        assert result == []

    def test_get_products_with_stock_status(self, db):
        p = _product(stock=5)
        db.query().all.return_value = [p]

        result = product_service.get_products(db)
        assert len(result) == 1
        assert result[0]["stock_status"] == "insufficient"

    def test_update_not_found(self, db):
        db.query().filter().first.return_value = None
        update = ProductUpdate(name="不存在")
        result = product_service.update_product(db, 999, update)
        assert result is None

    def test_delete_not_found(self, db):
        db.query().filter().first.return_value = None
        result = product_service.delete_product(db, 999)
        assert result is False
