"""组织架构业务逻辑 —— CRUD + 递归树构建 + 级联删除保护。"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import (
    OrgCreate,
    OrgResponse,
    OrgTreeResponse,
    OrgUpdate,
)


def _build_org_node(org: Organization) -> OrgResponse:
    """递归构建单个组织节点（含 children）。"""
    return OrgResponse(
        id=org.id,
        name=org.name,
        parent_id=org.parent_id,
        level=org.level,
        sort_order=org.sort_order,
        is_active=org.is_active,
        children=[_build_org_node(child) for child in org.children],
        created_at=org.created_at,
        updated_at=org.updated_at,
    )


def get_org_tree(db: Session) -> OrgTreeResponse:
    """获取完整组织树 —— 从根节点（parent_id IS NULL）开始递归。"""
    roots = (
        db.query(Organization)
        .filter(Organization.parent_id.is_(None))
        .order_by(Organization.sort_order)
        .all()
    )

    # 如果需要加载所有子节点，可以一次性查询然后内存组装，这里使用 relationship eager load
    # 由于 relationship 已配置 lazy select，树形递归会触发 N+1，但对于中小型组织树可以接受
    tree = [_build_org_node(root) for root in roots]
    return OrgTreeResponse(tree=tree)


def get_org_by_id(db: Session, org_id: int) -> Optional[Organization]:
    """按 ID 获取组织节点。"""
    return db.query(Organization).filter(Organization.id == org_id).first()


def create_org(db: Session, data: OrgCreate) -> Organization:
    """创建组织节点 —— 若指定 parent_id 则校验父节点存在且层级正确。"""
    if data.parent_id is not None:
        parent = get_org_by_id(db, data.parent_id)
        if not parent:
            raise ValueError(f"父组织 ID={data.parent_id} 不存在")
        if data.level != parent.level + 1:
            raise ValueError(
                f"层级不符合：父节点层级={parent.level}，当前应为 {parent.level + 1}，给定={data.level}"
            )

    instance = Organization(**data.model_dump())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update_org(db: Session, instance: Organization, data: OrgUpdate) -> Organization:
    """更新组织节点字段。"""
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance


def delete_org(db: Session, instance: Organization) -> None:
    """删除组织节点 —— 仅当无子节点时允许删除，否则抛出异常。"""
    children_count = (
        db.query(Organization)
        .filter(Organization.parent_id == instance.id)
        .count()
    )
    if children_count > 0:
        raise ValueError(
            f"无法删除『{instance.name}』：该节点下有 {children_count} 个子节点，请先删除子节点。"
        )
    db.delete(instance)
    db.commit()
