"""
项目管理 API 测试 (projects.py) — 6 个端点全覆盖。

12 阶段流转: 1线索→2商机→3需求→4方案→5报价→6谈判→7合同→8交付→9验收→10回款→11运维→12结项
"""
from datetime import date, datetime, timezone
from unittest.mock import MagicMock

import pytest


NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


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
    if obj.id is None:
        obj.id = 1
    if obj.created_at is None:
        obj.created_at = NOW
    if obj.updated_at is None:
        obj.updated_at = NOW


@pytest.mark.api
class TestCreateProject:
    def test_create_success(self):
        from app.api.v1.projects import create
        from app.schemas.project import ProjectCreate
        body = ProjectCreate(name="新项目")
        db = MagicMock()
        db.add, db.commit = MagicMock(), MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)
        result = create(body, db)
        assert result.code == 200
        assert result.data is not None

    def test_create_with_all_fields(self):
        from app.api.v1.projects import create
        from app.schemas.project import ProjectCreate
        body = ProjectCreate(name="完整", description="描述", stage=1,
                             start_date=date(2026, 3, 1), end_date=date(2026, 9, 30),
                             budget=5000000.00, actual_cost=0.00,
                             manager_id=10, org_id=2)
        db = MagicMock()
        db.add, db.commit = MagicMock(), MagicMock()
        db.refresh = MagicMock(side_effect=_fake_refresh)
        result = create(body, db)
        assert result.code == 200

    def test_create_missing_name(self):
        from pydantic import ValidationError
        from app.schemas.project import ProjectCreate
        with pytest.raises(ValidationError):
            ProjectCreate()

    def test_create_invalid_stage(self):
        from pydantic import ValidationError
        from app.schemas.project import ProjectCreate
        with pytest.raises(ValidationError):
            ProjectCreate(name="test", stage=0)
        with pytest.raises(ValidationError):
            ProjectCreate(name="test", stage=13)

    def test_create_negative_budget(self):
        from pydantic import ValidationError
        from app.schemas.project import ProjectCreate
        with pytest.raises(ValidationError):
            ProjectCreate(name="test", budget=-1)


@pytest.mark.api
class TestListProjects:
    def test_list_default(self):
        from app.api.v1.projects import list as list_projects
        db = mock_db_with(mock_project_row())
        result = list_projects(page=1, page_size=20, sort_order="desc", db=db)
        assert result.code == 200
        assert result.data.total == 1

    def test_list_filter_by_stage(self):
        from app.api.v1.projects import list as list_projects
        db = mock_db_with(mock_project_row(stage=7))
        result = list_projects(page=1, page_size=20, sort_order="desc",
                               stage=7, db=db)
        assert result.code == 200

    def test_list_search(self):
        from app.api.v1.projects import list as list_projects
        db = mock_db_with(mock_project_row())
        result = list_projects(page=1, page_size=20, sort_order="desc",
                               search="测试", db=db)
        assert result.code == 200

    def test_list_sort_asc(self):
        from app.api.v1.projects import list as list_projects
        db = mock_db_with(mock_project_row())
        result = list_projects(page=1, page_size=20, sort_order="asc", db=db)
        assert result.code == 200

    def test_list_empty(self):
        from app.api.v1.projects import list as list_projects
        db = mock_db_with(mock_project_row())
        db.all.return_value = []
        db.count.return_value = 0
        result = list_projects(page=1, page_size=20, sort_order="desc", db=db)
        assert result.code == 200
        assert result.data.total == 0

    def test_list_invalid_sort_order_validated_by_schema(self):
        from pydantic import ValidationError
        from app.schemas.project import ProjectListQuery
        with pytest.raises(ValidationError):
            ProjectListQuery(sort_order="bad")


@pytest.mark.api
class TestGetProject:
    def test_get_found(self):
        from app.api.v1.projects import get
        db = mock_db_with(mock_project_row(id=100))
        result = get(100, db)
        assert result.code == 200
        assert result.data.id == 100

    def test_get_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.projects import get
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            get(999, db)
        assert exc.value.status_code == 404


@pytest.mark.api
class TestUpdateProject:
    def test_update_name(self):
        from app.api.v1.projects import update
        from app.schemas.project import ProjectUpdate
        db = mock_db_with(mock_project_row())
        db.refresh = MagicMock(side_effect=_fake_refresh)
        result = update(1, ProjectUpdate(name="新名称"), db)
        assert result.code == 200

    def test_update_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.projects import update
        from app.schemas.project import ProjectUpdate
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            update(999, ProjectUpdate(name="x"), db)
        assert exc.value.status_code == 404


@pytest.mark.api
class TestUpdateProjectStage:
    def test_valid_transition(self):
        from app.api.v1.projects import update_stage
        from app.schemas.project import ProjectStageUpdate
        row = mock_project_row(stage=1)
        row.can_transition_to.return_value = True
        db = mock_db_with(row)
        db.refresh = MagicMock(side_effect=_fake_refresh)
        result = update_stage(1, ProjectStageUpdate(stage=2), db)
        assert result.code == 200

    def test_invalid_transition(self):
        from fastapi import HTTPException
        from app.api.v1.projects import update_stage
        from app.schemas.project import ProjectStageUpdate
        row = mock_project_row(stage=7)
        row.can_transition_to.return_value = False
        db = mock_db_with(row)
        with pytest.raises(HTTPException) as exc:
            update_stage(1, ProjectStageUpdate(stage=1), db)
        assert exc.value.status_code == 400

    def test_stage_not_found(self):
        from fastapi import HTTPException
        from app.api.v1.projects import update_stage
        from app.schemas.project import ProjectStageUpdate
        db = MagicMock()
        db.query.return_value = db
        db.filter.return_value = db
        db.first.return_value = None
        with pytest.raises(HTTPException) as exc:
            update_stage(999, ProjectStageUpdate(stage=2), db)
        assert exc.value.status_code == 404

    def test_invalid_stage_value(self):
        from pydantic import ValidationError
        from app.schemas.project import ProjectStageUpdate
        with pytest.raises(ValidationError):
            ProjectStageUpdate(stage=13)


@pytest.mark.api
class TestKanbanBoard:
    def test_kanban_returns_groups(self):
        from app.api.v1.projects import kanban
        db = mock_db_with(mock_project_row(stage=1))
        result = kanban(db=db)
        assert result.code == 200
        assert isinstance(result.data, list)

    def test_kanban_empty(self):
        from app.api.v1.projects import kanban
        db = mock_db_with(mock_project_row())
        db.all.return_value = []
        result = kanban(db=db)
        assert result.code == 200
        assert all(g.count == 0 for g in result.data)
