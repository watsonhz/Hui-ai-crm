"""
客户管理 API 测试 — 5 个端点全覆盖 (TASK-001 customer-crud)

POST   /api/v1/customers/      创建客户
GET    /api/v1/customers/      客户列表（分页+筛选+排序）
GET    /api/v1/customers/{id}  客户详情
PUT    /api/v1/customers/{id}  更新客户
DELETE /api/v1/customers/{id}  软删除客户
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


def mock_customer_row(**overrides):
    defaults = {
        "id": 1, "name": "张三", "company": "阿里巴巴",
        "contact": "李经理", "phone": "13800138000",
        "email": "test@example.com", "industry": "互联网",
        "level": "A", "status": "active", "source": "官网",
        "address": "杭州市余杭区", "notes": None,
        "created_at": NOW, "updated_at": NOW, "deleted_at": None,
    }
    defaults.update(overrides)
    row = MagicMock()
    for k, v in defaults.items():
        setattr(row, k, v)
    return row


def mock_db_session():
    db = MagicMock()
    db.query.return_value = db
    db.filter.return_value = db
    db.order_by.return_value = db
    db.offset.return_value = db
    db.limit.return_value = db
    db.count.return_value = 1
    db.all.return_value = [mock_customer_row()]
    db.first.return_value = mock_customer_row()
    return db


def _fake_refresh(obj):
    if not hasattr(obj, 'id') or obj.id is None:
        obj.id = 1
    if not hasattr(obj, 'created_at') or obj.created_at is None:
        obj.created_at = NOW
    if not hasattr(obj, 'updated_at') or obj.updated_at is None:
        obj.updated_at = NOW


# Redirect the backend/backend module path for the test
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent.parent.parent / "backend" / "backend"))


# ============================================================
# POST /customers — 创建客户
# ============================================================

@pytest.mark.api
class TestCreateCustomer:

    def test_create_success(self):
        from app.schemas.customer import CustomerCreate
        from app.services.customer_service import create_customer

        body = CustomerCreate(name="新客户", company="测试公司", level="B")
        db = MagicMock()
        db.add, db.commit = MagicMock(), MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)

        result = create_customer(db, body)
        assert result is not None
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_create_with_all_fields(self):
        from app.schemas.customer import CustomerCreate
        from app.services.customer_service import create_customer

        body = CustomerCreate(
            name="完整客户", company="完整公司", contact="王总",
            phone="13912345678", email="wang@test.com",
            industry="金融", level="A", source="地推",
            address="北京市朝阳区", notes="VIP 客户",
        )
        db = MagicMock()
        db.add, db.commit = MagicMock(), MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)

        result = create_customer(db, body)
        assert result is not None

    def test_create_missing_name(self):
        from pydantic import ValidationError
        from app.schemas.customer import CustomerCreate
        with pytest.raises(ValidationError):
            CustomerCreate()

    def test_create_invalid_phone(self):
        from pydantic import ValidationError
        from app.schemas.customer import CustomerCreate
        with pytest.raises(ValidationError):
            CustomerCreate(name="x", phone="12345")  # 不是手机号格式
        with pytest.raises(ValidationError):
            CustomerCreate(name="x", phone="12345678901")  # 首位不是 1[3-9]

    def test_create_invalid_level(self):
        from pydantic import ValidationError
        from app.schemas.customer import CustomerCreate
        with pytest.raises(ValidationError):
            CustomerCreate(name="x", level="X")  # 仅支持 A/B/C/D

    def test_create_invalid_email(self):
        from pydantic import ValidationError
        from app.schemas.customer import CustomerCreate
        with pytest.raises(ValidationError):
            CustomerCreate(name="x", email="not-an-email")

    def test_create_defaults(self):
        from app.schemas.customer import CustomerCreate
        body = CustomerCreate(name="默认客户")
        assert body.level is None  # schema 不设默认值，model 默认 C


# ============================================================
# GET /customers — 列表
# ============================================================

@pytest.mark.api
class TestListCustomers:

    def test_list_default(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db)

        assert total == 1
        assert len(items) == 1

    def test_list_paginated(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, page=2, page_size=10)
        assert total == 1

    def test_list_filter_by_name(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, name="张三")
        assert total == 1

    def test_list_filter_by_company(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, company="阿里")
        assert total == 1

    def test_list_filter_by_status(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, status="active")
        assert total == 1

    def test_list_filter_by_level(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, level="A")
        assert total == 1

    def test_list_filter_by_source(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, source="官网")
        assert total == 1

    def test_list_sort_by_name_asc(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, sort_order="name_asc")
        assert total == 1

    def test_list_sort_by_created_desc(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        items, total = get_customers(db, sort_order="created_desc")
        assert total == 1

    def test_list_empty(self):
        from app.services.customer_service import get_customers

        db = mock_db_session()
        db.all.return_value = []
        db.count.return_value = 0
        items, total = get_customers(db)

        assert total == 0
        assert items == []


# ============================================================
# GET /customers/{id} — 详情
# ============================================================

@pytest.mark.api
class TestGetCustomer:

    def test_get_found(self):
        from app.services.customer_service import get_customer_by_id

        db = mock_db_session()
        result = get_customer_by_id(db, 1)
        assert result.id == 1

    def test_get_not_found(self):
        from app.services.customer_service import (
            get_customer_by_id, CustomerNotFoundError,
        )

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        with pytest.raises(CustomerNotFoundError):
            get_customer_by_id(db, 999)


# ============================================================
# PUT /customers/{id} — 更新
# ============================================================

@pytest.mark.api
class TestUpdateCustomer:

    def test_update_name(self):
        from app.schemas.customer import CustomerUpdate
        from app.services.customer_service import update_customer

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = mock_customer_row(id=1)
        db.commit, db.refresh = MagicMock(), MagicMock()

        body = CustomerUpdate(name="新名字")
        result = update_customer(db, 1, body)
        assert result is not None

    def test_update_partial(self):
        """部分更新 — 只传 email 不改其他字段。"""
        from app.schemas.customer import CustomerUpdate
        from app.services.customer_service import update_customer

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = mock_customer_row(id=1)
        db.commit, db.refresh = MagicMock(), MagicMock()

        body = CustomerUpdate(email="new@test.com")
        result = update_customer(db, 1, body)
        assert result is not None

    def test_update_status(self):
        from app.schemas.customer import CustomerUpdate
        from app.services.customer_service import update_customer

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = mock_customer_row(id=1)
        db.commit, db.refresh = MagicMock(), MagicMock()

        body = CustomerUpdate(status="inactive")
        result = update_customer(db, 1, body)
        assert result is not None

    def test_update_not_found(self):
        from app.schemas.customer import CustomerUpdate
        from app.services.customer_service import (
            update_customer, CustomerNotFoundError,
        )

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        with pytest.raises(CustomerNotFoundError):
            update_customer(db, 999, CustomerUpdate(name="x"))

    def test_update_invalid_status(self):
        from pydantic import ValidationError
        from app.schemas.customer import CustomerUpdate
        with pytest.raises(ValidationError):
            CustomerUpdate(status="deleted")  # 仅 active/inactive


# ============================================================
# DELETE /customers/{id} — 软删除
# ============================================================

@pytest.mark.api
class TestDeleteCustomer:

    def test_delete_success(self):
        from app.services.customer_service import soft_delete_customer

        row = mock_customer_row(id=1)
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = row
        db.commit = MagicMock()

        soft_delete_customer(db, 1)
        # deleted_at 应被设置
        assert row.deleted_at is not None

    def test_delete_not_found(self):
        from app.services.customer_service import (
            soft_delete_customer, CustomerNotFoundError,
        )

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        with pytest.raises(CustomerNotFoundError):
            soft_delete_customer(db, 999)
