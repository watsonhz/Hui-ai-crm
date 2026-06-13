"""
项目管理 API 测试 (projects.py) — 6 个端点全覆盖。

POST   /                          — 创建项目
GET    /                          — 列表（分页+搜索+阶段筛选+排序）
GET    /{project_id}              — 详情
PUT    /{project_id}              — 更新
PUT    /{project_id}/stage        — 阶段流转（含校验）
GET    /board/kanban              — 看板视图

12 阶段流转: 1线索→2商机→3需求→4方案→5报价→6谈判→7合同→8交付→9验收→10回款→11运维→12结项
"""
from datetime import date, datetime, timezone
from unittest.mock import MagicMock

import pytest


# ============================================================
# Mock helpers
# ============================================================

def mock_project_row(**overrides):
    """构造模拟的 Project ORM 对象。"""
    defaults = {
        "id": 1,
        "name": "测试项目",
        "description": "测试项目描述",
        "stage": 1,
        "start_date": date(2026, 1, 1),
        "end_date": date(2026, 12, 31),
        "budget": 1000000.00,
        "actual_cost": 0.00,
        "manager_id": 1,
        "org_id": 1,
        "created_at": datetime(2026, 6, 1, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 6, 1, tzinfo=timezone.utc),
        "deleted_at": None,
    }
    defaults.update(overrides)
    mock = MagicMock()
    for k, v in defaults.items():
        setattr(mock, k, v)
    # can_transition_to 默认返回 True
    mock.can_transition_to = MagicMock(return_value=True)
    return mock


def mock_db_with(obj):
    """构造带 query 链的 mock DB。"""
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
# POST / — 创建项目
# ============================================================

@pytest.mark.api
class TestCreateProject:
    """创建项目端点测试。"""

    def test_create_success(self):
        """正常创建 — 必填字段 name。"""
        from app.api.v1.projects import create
        from app.schemas.project import ProjectCreate

        body = ProjectCreate(name="新项目")
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = create(body, db)

        assert result.code == 200
        assert result.data is not None
        db.add.assert_called_once()
        db.commit.assert_called_once()

    def test_create_with_all_fields(self):
        """全字段创建。"""
        from app.api.v1.projects import create
        from app.schemas.project import ProjectCreate

        body = ProjectCreate(
            name="完整项目",
            description="这是一个完整的项目",
            stage=1,
            start_date=date(2026, 3, 1),
            end_date=date(2026, 9, 30),
            budget=5000000.00,
            actual_cost=0.00,
            manager_id=10,
            org_id=2,
        )
        db = MagicMock()
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = create(body, db)
        assert result.code == 200

    def test_create_missing_name(self):
        """缺少必填字段 name。"""
        from pydantic import ValidationError
        from app.schemas.project import ProjectCreate

        with pytest.raises(ValidationError):
            ProjectCreate()

    def test_create_invalid_stage(self):
        """无效阶段 — 0 或 13。"""
        from pydantic import ValidationError
        from app.schemas.project import ProjectCreate

        with pytest.raises(ValidationError):
            ProjectCreate(name="test", stage=0)
        with pytest.raises(ValidationError):
            ProjectCreate(name="test", stage=13)

    def test_create_negative_budget(self):
        """负预算应被拒绝。"""
        from pydantic import ValidationError
        from app.schemas.project import ProjectCreate

        with pytest.raises(ValidationError):
            ProjectCreate(name="test", budget=-1)


# ============================================================
# GET / — 列表
# ============================================================

@pytest.mark.api
class TestListProjects:
    """项目列表端点测试。"""

    def test_list_default(self):
        """默认分页。"""
        from app.api.v1.projects import list as list_projects

        db = mock_db_with(mock_project_row())
        result = list_projects(db=db)

        assert result.code == 200
        assert result.data.total == 1
        assert result.data.page == 1
        assert len(result.data.items) == 1

    def test_list_filter_by_stage(self):
        """按阶段筛选 — stage=7 合同阶段。"""
        from app.api.v1.projects import list as list_projects

        db = mock_db_with(mock_project_row(stage=7))
        result = list_projects(stage=7, db=db)

        assert result.code == 200

    def test_list_search(self):
        """模糊搜索 — 按名称。"""
        from app.api.v1.projects import list as list_projects

        db = mock_db_with(mock_project_row())
        result = list_projects(search="测试", db=db)

        assert result.code == 200

    def test_list_sort_asc(self):
        """升序排列。"""
        from app.api.v1.projects import list as list_projects

        db = mock_db_with(mock_project_row())
        result = list_projects(sort_order="asc", db=db)

        assert result.code == 200

    def test_list_empty(self):
        """空列表。"""
        from app.api.v1.projects import list as list_projects

        db = mock_db_with(mock_project_row())
        db.all.return_value = []
        db.count.return_value = 0

        result = list_projects(db=db)

        assert result.code == 200
        assert result.data.total == 0

    def test_list_invalid_page(self):
        """非法分页参数。"""
        with pytest.raises(Exception):
            from app.api.v1.projects import list as list_projects
            list_projects(page=0, db=MagicMock())

    def test_list_invalid_stage_out_of_range(self):
        """阶段参数超界。"""
        with pytest.raises(Exception):
            from app.api.v1.projects import list as list_projects
            list_projects(stage=13, db=MagicMock())


# ============================================================
# GET /{project_id} — 详情
# ============================================================

@pytest.mark.api
class TestGetProject:
    """项目详情端点测试。"""

    def test_get_found(self):
        """正常获取。"""
        from app.api.v1.projects import get

        db = mock_db_with(mock_project_row(id=100))
        result = get(100, db)

        assert result.code == 200
        assert result.data.id == 100

    def test_get_not_found(self):
        """不存在 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.projects import get

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        with pytest.raises(HTTPException) as exc:
            get(999, db)
        assert exc.value.status_code == 404


# ============================================================
# PUT /{project_id} — 更新
# ============================================================

@pytest.mark.api
class TestUpdateProject:
    """项目更新端点测试。"""

    def test_update_name(self):
        """更新名称。"""
        from app.api.v1.projects import update
        from app.schemas.project import ProjectUpdate

        db = mock_db_with(mock_project_row())
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        body = ProjectUpdate(name="新项目名称")
        result = update(1, body, db)

        assert result.code == 200

    def test_update_not_found(self):
        """更新不存在的项目 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.projects import update
        from app.schemas.project import ProjectUpdate

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        body = ProjectUpdate(name="x")
        with pytest.raises(HTTPException) as exc:
            update(999, body, db)
        assert exc.value.status_code == 404


# ============================================================
# PUT /{project_id}/stage — 阶段流转
# ============================================================

@pytest.mark.api
class TestUpdateProjectStage:
    """项目阶段流转端点测试。"""

    def test_valid_transition(self):
        """合法流转 — 线索(1)→商机(2)。"""
        from app.api.v1.projects import update_stage
        from app.schemas.project import ProjectStageUpdate

        project = mock_project_row(stage=1)
        project.can_transition_to.return_value = True
        db = mock_db_with(project)
        db.add = MagicMock()
        db.commit = MagicMock()
        db.refresh = MagicMock()

        body = ProjectStageUpdate(stage=2)
        result = update_stage(1, body, db)

        assert result.code == 200

    def test_invalid_transition(self):
        """非法流转 — 合同(7)不能跳到线索(1)。"""
        from fastapi import HTTPException
        from app.api.v1.projects import update_stage
        from app.schemas.project import ProjectStageUpdate

        project = mock_project_row(stage=7)
        project.can_transition_to.return_value = False
        db = mock_db_with(project)

        body = ProjectStageUpdate(stage=1)  # 7→1 不允许
        with pytest.raises(HTTPException) as exc:
            update_stage(1, body, db)
        assert exc.value.status_code == 400

    def test_update_stage_not_found(self):
        """项目不存在 — 404。"""
        from fastapi import HTTPException
        from app.api.v1.projects import update_stage
        from app.schemas.project import ProjectStageUpdate

        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None

        body = ProjectStageUpdate(stage=2)
        with pytest.raises(HTTPException) as exc:
            update_stage(999, body, db)
        assert exc.value.status_code == 404

    def test_invalid_stage_value(self):
        """非法 stage 值。"""
        from pydantic import ValidationError
        from app.schemas.project import ProjectStageUpdate

        with pytest.raises(ValidationError):
            ProjectStageUpdate(stage=0)
        with pytest.raises(ValidationError):
            ProjectStageUpdate(stage=13)


# ============================================================
# GET /board/kanban — 看板视图
# ============================================================

@pytest.mark.api
class TestKanbanBoard:
    """看板端点测试。"""

    def test_kanban_returns_groups(self):
        """看板返回 12 阶段分组。"""
        from app.api.v1.projects import kanban

        db = mock_db_with(mock_project_row(stage=1))
        result = kanban(db=db)

        assert result.code == 200
        assert isinstance(result.data, list)

    def test_kanban_empty(self):
        """无项目时看板返回空分组。"""
        from app.api.v1.projects import kanban

        db = mock_db_with(mock_project_row())
        db.all.return_value = []

        result = kanban(db=db)

        assert result.code == 200
        assert all(g.count == 0 for g in result.data)
