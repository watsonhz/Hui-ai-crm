"""
组织层级 API 测试 (organizations.py) — 5 个端点全覆盖。

POST   /                   — 创建组织（含父级校验）
GET    /tree               — 树形结构
PUT    /{org_id}           — 更新（含自引用检查）
DELETE /{org_id}           — 软删除（含子组织检查）

组织类型: company(公司) / dept(部门) / team(团队)
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest


# ============================================================
# Mock helpers
# ============================================================

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
    """构造带 query 链的 mock DB。"""
    db = MagicMock()
    db.query.return_value = db
    db.filter.return_value = db
    db.order_by.return_value = db
    db.count.return_value = 0
    db.all.return_value = [obj]
    db.first.return_value = obj
    return db


# ============================================================
# POST / — 创建组织
# ============================================================

@pytest.mark.api
class TestCreateOrganization:
    """创建组织端点测试。"""

    def test_create_root_org(self):
        """创建顶级组织（无 parent_id）。"""
        from app.api.v1.organizations import create
        from app.schemas.organization import OrganizationCreate

        body = OrganizationCreate(name="总公司", org_type="company")
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = create(body, db)

        assert result.code == 200
        assert result.data is not None

    def test_create_child_org(self):
        """创建子组织 — parent_id 指向存在的父级。"""
        from app.api.v1.organizations import create
        from app.schemas.organization import OrganizationCreate

        parent = mock_org_row(id=1, org_type="company")
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()
        # 第一次 query 用于查 parent
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = parent

        body = OrganizationCreate(
            name="研发部", parent_id=1, org_type="dept"
        )
        result = create(body, db)

        assert result.code == 200

    def test_create_parent_not_found(self):
        """父级不存在 — 400。"""
        from fastapi import HTTPException
        from app.api.v1.organizations import create
        from app.schemas.organization import OrganizationCreate

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None  # parent 不存在

        body = OrganizationCreate(
            name="孤儿部门", parent_id=999, org_type="dept"
        )
        with pytest.raises(HTTPException) as exc:
            create(body, db)
        assert exc.value.status_code == 400
        assert "父级" in exc.value.detail

    def test_create_invalid_org_type(self):
        """非法组织类型。"""
        from pydantic import ValidationError
        from app.schemas.organization import OrganizationCreate

        with pytest.raises(ValidationError):
            OrganizationCreate(name="x", org_type="invalid")

    def test_create_defaults(self):
        """默认值 — org_type 默认 dept, sort_order 默认 0。"""
        from app.schemas.organization import OrganizationCreate

        body = OrganizationCreate(name="默认部门")
        assert body.org_type == "dept"
        assert body.sort_order == 0

    def test_create_negative_sort_order(self):
        """负的 sort_order — 应被拒绝。"""
        from pydantic import ValidationError
        from app.schemas.organization import OrganizationCreate

        with pytest.raises(ValidationError):
            OrganizationCreate(name="x", sort_order=-1)


# ============================================================
# GET /tree — 树形结构
# ============================================================

@pytest.mark.api
class TestOrganizationTree:
    """组织树端点测试。"""

    def test_tree_empty(self):
        """无组织时返回空列表。"""
        from app.api.v1.organizations import tree

        db = mock_db_with(mock_org_row())
        db.all.return_value = []

        result = tree(db=db)

        assert result.code == 200
        assert result.data == []

    def test_tree_single_root(self):
        """单根节点。"""
        from app.api.v1.organizations import tree

        db = mock_db_with(mock_org_row(id=1, name="总公司", org_type="company"))
        result = tree(db=db)

        assert result.code == 200
        assert len(result.data) == 1
        assert result.data[0].name == "总公司"
        assert result.data[0].children == []

    def test_tree_with_children(self):
        """父子结构 — 子组织挂在父组织下。"""
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

    def test_tree_sort_order_respected(self):
        """按 sort_order 排列。"""
        from app.api.v1.organizations import tree

        a = mock_org_row(id=1, name="A", sort_order=2)
        b = mock_org_row(id=2, name="B", sort_order=1)
        db = mock_db_with(a)
        db.all.return_value = [b, a]  # 模拟排序后

        result = tree(db=db)

        assert result.code == 200
        assert result.data[0].name == "B"  # sort_order 1 排在前


# ============================================================
# PUT /{org_id} — 更新
# ============================================================

@pytest.mark.api
class TestUpdateOrganization:
    """组织更新端点测试。"""

    def test_update_name(self):
        """更新名称。"""
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate

        db = mock_db_with(mock_org_row(id=1))
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        body = OrganizationUpdate(name="新部门名称")
        result = update(1, body, db)

        assert result.code == 200

    def test_update_self_parent(self):
        """将 parent_id 设为自身 — 400。"""
        from fastapi import HTTPException
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate

        db = mock_db_with(mock_org_row(id=1))

        body = OrganizationUpdate(parent_id=1)
        with pytest.raises(HTTPException) as exc:
            update(1, body, db)
        assert exc.value.status_code == 400
        assert "自身" in exc.value.detail

    def test_update_parent_not_found(self):
        """父级不存在 — 400。"""
        from fastapi import HTTPException
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        # 第一次 first 返回 org 存在，第二次 first 返回 None（parent 不存在）
        db.first.side_effect = [mock_org_row(id=1), None]

        body = OrganizationUpdate(parent_id=999)
        with pytest.raises(HTTPException) as exc:
            update(1, body, db)
        assert exc.value.status_code == 400

    def test_update_not_found(self):
        """组织不存在 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.organizations import update
        from app.schemas.organization import OrganizationUpdate

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        body = OrganizationUpdate(name="x")
        with pytest.raises(HTTPException) as exc:
            update(999, body, db)
        assert exc.value.status_code == 404

    def test_update_invalid_org_type(self):
        """非法 org_type。"""
        from pydantic import ValidationError
        from app.schemas.organization import OrganizationUpdate

        with pytest.raises(ValidationError):
            OrganizationUpdate(org_type="invalid")


# ============================================================
# DELETE /{org_id} — 软删除
# ============================================================

@pytest.mark.api
class TestDeleteOrganization:
    """组织删除端点测试。"""

    def test_delete_leaf_org(self):
        """删除叶子节点 — 无子组织，可删除（软删除）。"""
        from app.api.v1.organizations import delete

        db = mock_db_with(mock_org_row(id=1))
        db.add = MagicMock()
        db.commit = MagicMock()
        db.count.return_value = 0  # 无子组织

        result = delete(1, db)

        assert result.code == 200
        assert result.message == "删除成功"

    def test_delete_with_children(self):
        """有子组织时删除 — 400。"""
        from fastapi import HTTPException
        from app.api.v1.organizations import delete

        db = mock_db_with(mock_org_row(id=1))
        db.count.return_value = 3  # 有 3 个子组织

        with pytest.raises(HTTPException) as exc:
            delete(1, db)
        assert exc.value.status_code == 400
        assert "子组织" in exc.value.detail

    def test_delete_not_found(self):
        """删除不存在的组织 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.organizations import delete

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        with pytest.raises(HTTPException) as exc:
            delete(999, db)
        assert exc.value.status_code == 404
