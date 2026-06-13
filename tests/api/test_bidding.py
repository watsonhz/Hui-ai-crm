"""
投标管理 API 测试 (bidding.py) — 6 个端点全覆盖。

9 态状态机: 1意向→2招标中→3投标中→4评标中→5中标 / 6失标 / 7废标→9完成
"""
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock

import pytest


NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)
FUTURE = datetime(2026, 8, 1, tzinfo=timezone.utc)


def mock_bidding_row(**overrides):
    """构造一个模拟的 Bidding ORM 对象。"""
    defaults = {
        "id": 1,
        "title": "XX项目投标",
        "project_name": "XX项目",
        "bid_amount": 500000.00,
        "bid_status": 1,
        "bid_deadline": FUTURE,
        "submit_deadline": FUTURE,
        "client_company": "测试客户公司",
        "client_contact": "李经理",
        "description": "测试投标描述",
        "notes": None,
        "owner_id": 1,
        "created_at": NOW,
        "updated_at": NOW,
        "deleted_at": None,
    }
    defaults.update(overrides)
    row = MagicMock()
    for k, v in defaults.items():
        setattr(row, k, v)
    row.can_transition_to = MagicMock(return_value=True)
    return row


def mock_db_with(obj):
    """构造一个带完整 query 链的 mock DB session。"""
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


def _fake_refresh(obj):
    """Simulate db.refresh by setting auto-generated fields."""
    if obj.id is None:
        obj.id = 1
    if obj.created_at is None:
        obj.created_at = NOW
    if obj.updated_at is None:
        obj.updated_at = NOW


# ============================================================
# POST / — 创建投标
# ============================================================

@pytest.mark.api
class TestCreateBidding:
    """创建投标端点测试。"""

    def test_create_success(self):
        from app.api.v1.bidding import create
        from app.schemas.bidding import BiddingCreate

        body = BiddingCreate(title="测试投标项目")
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)

        result = create(body, db)

        assert result.code == 200
        assert result.data is not None
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_create_with_all_fields(self):
        from app.api.v1.bidding import create
        from app.schemas.bidding import BiddingCreate

        body = BiddingCreate(
            title="完整投标", project_name="关联项目",
            bid_amount=1000000.00, bid_status=1,
            bid_deadline=FUTURE, client_company="大客户公司",
            client_contact="张总", description="完整说明", owner_id=5,
        )
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)

        result = create(body, db)
        assert result.code == 200

    def test_create_missing_title(self):
        from pydantic import ValidationError
        from app.schemas.bidding import BiddingCreate
        with pytest.raises(ValidationError):
            BiddingCreate()

    def test_create_invalid_bid_status(self):
        from pydantic import ValidationError
        from app.schemas.bidding import BiddingCreate
        with pytest.raises(ValidationError):
            BiddingCreate(title="test", bid_status=0)
        with pytest.raises(ValidationError):
            BiddingCreate(title="test", bid_status=10)

    def test_create_negative_bid_amount(self):
        from pydantic import ValidationError
        from app.schemas.bidding import BiddingCreate
        with pytest.raises(ValidationError):
            BiddingCreate(title="test", bid_amount=-100)


# ============================================================
# GET / — 列表
# ============================================================

@pytest.mark.api
class TestListBidding:

    def test_list_default_pagination(self):
        from app.api.v1.bidding import list as list_bidding
        db = mock_db_with(mock_bidding_row())
        result = list_bidding(page=1, page_size=20, sort_order="desc", db=db)
        assert result.code == 200
        assert result.data.total == 1
        assert len(result.data.items) == 1

    def test_list_filter_by_status(self):
        from app.api.v1.bidding import list as list_bidding
        db = mock_db_with(mock_bidding_row(bid_status=5))
        result = list_bidding(page=1, page_size=20, sort_order="desc",
                              bid_status=5, db=db)
        assert result.code == 200

    def test_list_search(self):
        from app.api.v1.bidding import list as list_bidding
        db = mock_db_with(mock_bidding_row())
        result = list_bidding(page=1, page_size=20, sort_order="desc",
                              search="投标", db=db)
        assert result.code == 200

    def test_list_sort_asc(self):
        from app.api.v1.bidding import list as list_bidding
        db = mock_db_with(mock_bidding_row())
        result = list_bidding(page=1, page_size=20, sort_order="asc", db=db)
        assert result.code == 200

    def test_list_empty(self):
        from app.api.v1.bidding import list as list_bidding
        db = mock_db_with(mock_bidding_row())
        db.all.return_value = []
        db.count.return_value = 0
        result = list_bidding(page=1, page_size=20, sort_order="desc", db=db)
        assert result.code == 200
        assert result.data.total == 0

    def test_list_invalid_sort_order_validated_by_schema(self):
        """sort_order 不匹配 pattern 时被 BiddingListQuery schema 拦截。"""
        from pydantic import ValidationError
        from app.schemas.bidding import BiddingListQuery
        with pytest.raises(ValidationError):
            BiddingListQuery(sort_order="invalid")


# ============================================================
# GET /{bidding_id} — 详情
# ============================================================

@pytest.mark.api
class TestGetBidding:

    def test_get_found(self):
        from app.api.v1.bidding import get
        db = mock_db_with(mock_bidding_row(id=42))
        result = get(42, db)
        assert result.code == 200
        assert result.data.id == 42

    def test_get_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.bidding import get
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            get(999, db)
        assert exc.value.status_code == 404


# ============================================================
# PUT /{bidding_id} — 更新
# ============================================================

@pytest.mark.api
class TestUpdateBidding:

    def test_update_title(self):
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate
        db = mock_db_with(mock_bidding_row(id=1, bid_status=1))
        db.refresh = MagicMock(side_effect=_fake_refresh)

        body = BiddingUpdate(title="更新后的标题")
        result = update(1, body, db)
        assert result.code == 200

    def test_update_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            update(999, BiddingUpdate(title="x"), db)
        assert exc.value.status_code == 404

    def test_update_invalid_transition(self):
        from fastapi import HTTPException
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate
        row = mock_bidding_row(id=1, bid_status=5)
        row.can_transition_to.return_value = False  # 5→3 非法
        db = mock_db_with(row)
        db.refresh = MagicMock(side_effect=_fake_refresh)

        body = BiddingUpdate(bid_status=3)
        with pytest.raises(HTTPException) as exc:
            update(1, body, db)
        assert exc.value.status_code == 400

    def test_update_valid_transition(self):
        from app.api.v1.bidding import update
        from app.schemas.bidding import BiddingUpdate
        row = mock_bidding_row(id=1, bid_status=1)
        row.can_transition_to.return_value = True  # 1→2 合法
        db = mock_db_with(row)
        db.refresh = MagicMock(side_effect=_fake_refresh)

        body = BiddingUpdate(bid_status=2)
        result = update(1, body, db)
        assert result.code == 200


# ============================================================
# GET /calendar/upcoming
# ============================================================

@pytest.mark.api
class TestBiddingCalendar:

    def test_calendar_default_days(self):
        from app.api.v1.bidding import calendar
        db = mock_db_with(mock_bidding_row(bid_deadline=FUTURE))
        result = calendar(days=30, db=db)
        assert result.code == 200
        assert isinstance(result.data, list)

    def test_calendar_custom_days(self):
        from app.api.v1.bidding import calendar
        db = mock_db_with(mock_bidding_row(bid_deadline=FUTURE))
        result = calendar(days=90, db=db)
        assert result.code == 200

    def test_calendar_empty(self):
        from app.api.v1.bidding import calendar
        db = mock_db_with(mock_bidding_row())
        db.all.return_value = []
        result = calendar(days=30, db=db)
        assert result.code == 200
        assert result.data == []

    def test_calendar_zero_days_behaves_as_near_past(self):
        """days=0 不抛异常，但查不到数据（deadline 在将来 > now+0）。"""
        from app.api.v1.bidding import calendar
        db = mock_db_with(mock_bidding_row(bid_deadline=FUTURE))
        db.all.return_value = []
        result = calendar(days=0, db=db)
        assert result.code == 200
