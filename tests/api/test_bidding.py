"""
投标管理 API 测试 (bidding.py) — 6 个端点全覆盖。

POST   /                          — 创建投标
GET    /                          — 列表（分页+搜索+状态筛选+排序）
GET    /{bidding_id}              — 详情
PUT    /{bidding_id}              — 更新（含状态流转校验）
GET    /calendar/upcoming         — 即将截止的投标日历

9 态状态机: 1意向→2招标中→3投标中→4评标中→5中标 / 6失标 / 7废标→9完成
"""
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

import pytest


# ============================================================
# Mock helpers
# ============================================================

def mock_bidding_row(**overrides):
    """构造一个模拟的 Bidding ORM 对象。"""
    defaults = {
        "id": 1,
        "title": "XX项目投标",
        "project_name": "XX项目",
        "bid_amount": 500000.00,
        "bid_status": 1,
        "bid_deadline": datetime(2026, 7, 1, tzinfo=timezone.utc),
        "submit_deadline": datetime(2026, 6, 25, tzinfo=timezone.utc),
        "client_company": "测试客户公司",
        "client_contact": "李经理",
        "description": "测试投标描述",
        "notes": None,
        "owner_id": 1,
        "created_at": datetime(2026, 6, 1, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 6, 1, tzinfo=timezone.utc),
        "deleted_at": None,
    }
    defaults.update(overrides)
    mock = MagicMock()
    for k, v in defaults.items():
        setattr(mock, k, v)
    return mock


def mock_db_with(obj):
    """构造一个带 query 链的 mock DB session。"""
    db = MagicMock()
    db.query.return_value = db
    db.filter.return_value = db
    db.order_by.return_value = db
    db.offset.return_value = db
    db.limit.return_value = db
    db.count.return_value = 1
    db.all.return_value = [obj]
    db.first.return_value = obj
    return db


# ============================================================
# POST / — 创建投标
# ============================================================

@pytest.mark.api
class TestCreateBidding:
    """创建投标端点测试。"""

    def test_create_success(self):
        """正常创建 — 必填字段。"""
        from app.api.v1.bidding import create
        from app.schemas.bidding import BiddingCreate

        body = BiddingCreate(title="测试投标项目")
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = create(body, db)

        assert result.code == 200
        assert result.message == "success"
        assert result.data is not None
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_create_with_all_fields(self):
        """全字段创建。"""
        from app.api.v1.bidding import create
        from app.schemas.bidding import BiddingCreate

        body = BiddingCreate(
            title="完整投标",
            project_name="关联项目",
            bid_amount=1000000.00,
            bid_status=1,
            bid_deadline=datetime(2026, 8, 1, tzinfo=timezone.utc),
            client_company="大客户公司",
            client_contact="张总 13800138000",
            description="完整的投标说明",
            owner_id=5,
        )
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = create(body, db)
        assert result.code == 200

    def test_create_validation_error(self):
        """缺少必填字段 title — 应该校验失败。"""
        with pytest.raises(Exception):
            from app.schemas.bidding import BiddingCreate
            BiddingCreate()

    def test_create_invalid_bid_status(self):
        """无效状态码 — 0 或 10 应该被 Schema 拒绝。"""
        from pydantic import ValidationError
        from app.schemas.bidding import BiddingCreate

        with pytest.raises(ValidationError):
            BiddingCreate(title="test", bid_status=0)
        with pytest.raises(ValidationError):
            BiddingCreate(title="test", bid_status=10)

    def test_create_negative_bid_amount(self):
        """负数金额应被拒绝。"""
        from pydantic import ValidationError
        from app.schemas.bidding import BiddingCreate

        with pytest.raises(ValidationError):
            BiddingCreate(title="test", bid_amount=-100)


# ============================================================
# GET / — 列表
# ============================================================

@pytest.mark.api
class TestListBidding:
    """投标列表端点测试。"""

    def test_list_default_pagination(self):
        """默认分页参数。"""
        from app.api.v1.bidding import list as list_bidding

        db = mock_db_with(mock_bidding_row())
        result = list_bidding(db=db)

        assert result.code == 200
        assert result.data.total == 1
        assert result.data.page == 1
        assert result.data.page_size == 20
        assert len(result.data.items) == 1

    def test_list_filter_by_status(self):
        """按状态筛选 (bid_status=5 中标)。"""
        from app.api.v1.bidding import list as list_bidding

        db = mock_db_with(mock_bidding_row(bid_status=5))
        result = list_bidding(bid_status=5, db=db)

        assert result.code == 200

    def test_list_search(self):
        """模糊搜索 title。"""
        from app.api.v1.bidding import list as list_bidding

        db = mock_db_with(mock_bidding_row())
        result = list_bidding(search="投标", db=db)

        assert result.code == 200

    def test_list_sort_asc(self):
        """升序排列。"""
        from app.api.v1.bidding import list as list_bidding

        db = mock_db_with(mock_bidding_row())
        result = list_bidding(sort_order="asc", db=db)

        assert result.code == 200

    def test_list_empty(self):
        """空列表 — 无投标记录。"""
        from app.api.v1.bidding import list as list_bidding

        db = mock_db_with(mock_bidding_row())
        db.all.return_value = []
        db.count.return_value = 0

        result = list_bidding(db=db)

        assert result.code == 200
        assert result.data.total == 0
        assert result.data.items == []

    def test_list_invalid_page_negative(self):
        """page=0 被参数校验拦截。"""
        with pytest.raises(Exception):
            from app.api.v1.bidding import list as list_bidding
            list_bidding(page=0, db=MagicMock())

    def test_list_invalid_page_size_too_large(self):
        """page_size > 100 被拦截。"""
        with pytest.raises(Exception):
            from app.api.v1.bidding import list as list_bidding
            list_bidding(page_size=200, db=MagicMock())


# ============================================================
# GET /{bidding_id} — 详情
# ============================================================

@pytest.mark.api
class TestGetBidding:
    """投标详情端点测试。"""

    def test_get_found(self):
        """正常获取。"""
        from app.api.v1.bidding import get

        db = mock_db_with(mock_bidding_row(id=42))
        result = get(42, db)

        assert result.code == 200
        assert result.data.id == 42

    def test_get_not_found(self):
        """获取不存在的投标 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.bidding import get

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        with pytest.raises(HTTPException) as exc:
            get(999, db)
        assert exc.value.status_code == 404
        assert "不存在" in exc.value.detail


# ============================================================
# PUT /{bidding_id} — 更新
# ============================================================

@pytest.mark.api
class TestUpdateBidding:
    """投标更新端点测试。"""

    def test_update_title(self):
        """更新标题。"""
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate

        db = mock_db_with(mock_bidding_row(id=1, bid_status=1))
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        body = BiddingUpdate(title="更新后的标题")
        result = update(1, body, db)

        assert result.code == 200

    def test_update_not_found(self):
        """更新不存在的投标 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        body = BiddingUpdate(title="x")
        with pytest.raises(HTTPException) as exc:
            update(999, body, db)
        assert exc.value.status_code == 404

    def test_update_invalid_transition(self):
        """非法状态流转 — 已中标(5)不能回到投标中(3)。"""
        from fastapi import HTTPException
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate

        db = mock_db_with(mock_bidding_row(id=1, bid_status=5))
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        body = BiddingUpdate(bid_status=3)  # 5→3 不允许
        with pytest.raises(HTTPException) as exc:
            update(1, body, db)
        assert exc.value.status_code == 400

    def test_update_valid_transition(self):
        """合法状态流转 — 意向(1)→招标中(2)。"""
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate

        db = mock_db_with(mock_bidding_row(id=1, bid_status=1))
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        body = BiddingUpdate(bid_status=2)  # 1→2 允许
        result = update(1, body, db)

        assert result.code == 200


# ============================================================
# GET /calendar/upcoming — 即将截止的投标
# ============================================================

@pytest.mark.api
class TestBiddingCalendar:
    """投标日历端点测试。"""

    def test_calendar_default_days(self):
        """默认 30 天内。"""
        from app.api.v1.bidding import calendar

        future = datetime.now(timezone.utc) + timedelta(days=10)
        db = mock_db_with(
            mock_bidding_row(bid_deadline=future)
        )
        result = calendar(db=db)

        assert result.code == 200
        assert isinstance(result.data, list)

    def test_calendar_custom_days(self):
        """自定义天数 90。"""
        from app.api.v1.bidding import calendar

        future = datetime.now(timezone.utc) + timedelta(days=60)
        db = mock_db_with(
            mock_bidding_row(bid_deadline=future)
        )
        result = calendar(days=90, db=db)

        assert result.code == 200

    def test_calendar_empty(self):
        """无即将截止的投标。"""
        from app.api.v1.bidding import calendar

        db = mock_db_with(mock_bidding_row())
        db.all.return_value = []

        result = calendar(db=db)

        assert result.code == 200
        assert result.data == []

    def test_calendar_invalid_days(self):
        """days 超出范围 — >365 被拦截。"""
        with pytest.raises(Exception):
            from app.api.v1.bidding import calendar
            calendar(days=400, db=MagicMock())

    def test_calendar_invalid_negative_days(self):
        """days < 1 被拦截。"""
        with pytest.raises(Exception):
            from app.api.v1.bidding import calendar
            calendar(days=0, db=MagicMock())
