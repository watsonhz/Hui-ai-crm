"""
组织层级 API 测试 (organizations.py) — 5 个端点全覆盖。

组织类型: company(公司) / dept(部门) / team(团队)
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest


NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


def mock_org_row(**overrides):
    """构造模拟的 Organization ORM 对象。"""
    defaults = {
        "id": 1,
        "name": "技术部",
        "parent_id": None,
        "org_type": "dept",
        "description": "技术研发部门",
        "manager_id": 5,
        "sort_order": 0,
        "created_at": NOW,
        "updated_at": NOW,
        "deleted_at": None,
    }
    defaults.update(overrides)
    row = MagicMock()
    for k, v in defaults.items():
        setattr(row, k, v)
    return row


def mock_db_with(obj):
    db = MagicMock()
    db.query.return_value = db
    db.filter.return_value = db
    db.order_by.return_value = db
    db.count.return_value = 0
    db.all.return_value = [obj]
    db.first.return_value = obj
    return db


def _fake_refresh(obj):
    if obj.id is None:
        obj.id = 1
    if obj.created_at is None:
        obj.created_at = NOW
    if obj.updated_at is None:
        obj.updated_at = NOW


@pytest.mark.api
class TestCreateOrganization:
    def test_create_root_org(self):
        from app.api.v1.organizations import create
        from app.schemas.organization import OrganizationCreate
        body = OrganizationCreate(name="总公司", org_type="company")
        db = MagicMock()
        db.add, db.commit = MagicMock(), MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)
        result = create(body, db)
        assert result.code == 200

    def test_create_child_org(self):
        from app.api.v1.organizations import create
        from app.schemas.organization import OrganizationCreate
        parent = mock_org_row(id=1, org_type="company")
        db = MagicMock()
        db.add, db.commit = MagicMock(), MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = parent

        body = OrganizationCreate(name="研发部", parent_id=1, org_type="dept")
        result = create(body, db)
        assert result.code == 200

    def test_create_parent_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.organizations import create
        from app.schemas.organization import OrganizationCreate
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            create(OrganizationCreate(name="孤儿", parent_id=999, org_type="dept"), db)
        assert exc.value.status_code == 400
        assert "父级" in exc.value.detail

    def test_create_invalid_org_type(self):
        from pydantic import ValidationError
        from app.schemas.organization import OrganizationCreate
        with pytest.raises(ValidationError):
            OrganizationCreate(name="x", org_type="invalid")

    def test_create_defaults(self):
        from app.schemas.organization import OrganizationCreate
        body = OrganizationCreate(name="默认部门")
        assert body.org_type == "dept"
        assert body.sort_order == 0

    def test_create_negative_sort_order(self):
        from pydantic import ValidationError
        from app.schemas.organization import OrganizationCreate
        with pytest.raises(ValidationError):
            OrganizationCreate(name="x", sort_order=-1)


@pytest.mark.api
class TestOrganizationTree:
    def test_tree_empty(self):
        from app.api.v1.organizations import tree
        db = mock_db_with(mock_org_row())
        db.all.return_value = []
        result = tree(db=db)
        assert result.code == 200
        assert result.data == []

    def test_tree_single_root(self):
        from app.api.v1.organizations import tree
        db = mock_db_with(mock_org_row(id=1, name="总公司", org_type="company"))
        result = tree(db=db)
        assert result.code == 200
        assert len(result.data) == 1
        assert result.data[0].children == []

    def test_tree_with_children(self):
        from app.api.v1.organizations import tree
        parent = mock_org_row(id=1, name="总公司", org_type="company")
        child = mock_org_row(id=2, name="研发部", parent_id=1, org_type="dept")
        db = mock_db_with(parent)
        db.all.return_value = [parent, child]
        result = tree(db=db)
        assert result.code == 200
        assert len(result.data) == 1
        assert len(result.data[0].children) == 1
        assert result.data[0].children[0].name == "研发部"

    def test_tree_sort_order(self):
        from app.api.v1.organizations import tree
        b = mock_org_row(id=1, name="B", sort_order=1)
        a = mock_org_row(id=2, name="A", sort_order=2)
        db = mock_db_with(a)
        db.all.return_value = [b, a]
        result = tree(db=db)
        assert result.data[0].name == "B"


@pytest.mark.api
class TestUpdateOrganization:
    def test_update_name(self):
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate
        db = mock_db_with(mock_org_row(id=1))
        db.refresh = MagicMock(side_effect=_fake_refresh)
        result = update(1, OrganizationUpdate(name="新名称"), db)
        assert result.code == 200

    def test_update_self_parent(self):
        from fastapi import HTTPException
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate
        db = mock_db_with(mock_org_row(id=1))
        with pytest.raises(HTTPException) as exc:
            update(1, OrganizationUpdate(parent_id=1), db)
        assert exc.value.status_code == 400
        assert "自身" in exc.value.detail

    def test_update_parent_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.side_effect = [mock_org_row(id=1), None]
        with pytest.raises(HTTPException) as exc:
            update(1, OrganizationUpdate(parent_id=999), db)
        assert exc.value.status_code == 400

    def test_update_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            update(999, OrganizationUpdate(name="x"), db)
        assert exc.value.status_code == 404

    def test_update_invalid_org_type(self):
        from pydantic import ValidationError
        from app.schemas.organization import OrganizationUpdate
        with pytest.raises(ValidationError):
            OrganizationUpdate(org_type="invalid")


@pytest.mark.api
class TestDeleteOrganization:
    def test_delete_leaf_org(self):
        from app.api.v1.organizations import delete
        db = mock_db_with(mock_org_row(id=1))
        db.count.return_value = 0
        result = delete(1, db)
        assert result.code == 200

    def test_delete_with_children(self):
        from fastapi import HTTPException
        from app.api.v1.organizations import delete
        db = mock_db_with(mock_org_row(id=1))
        db.count.return_value = 3
        with pytest.raises(HTTPException) as exc:
            delete(1, db)
        assert exc.value.status_code == 400
        assert "子组织" in exc.value.detail

    def test_delete_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.organizations import delete
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            delete(999, db)
        assert exc.value.status_code == 404
