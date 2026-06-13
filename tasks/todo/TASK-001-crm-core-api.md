---
task_id: TASK-001
title: CRM核心业务CRUD API（招投标+项目+组织层级）
assignee: pc3
role: backend-architect
priority: P0 (最高)
deadline: 2026-06-20
branch: feature/TASK-001-crm-core-api
dependencies: [TASK-000-database-init]
tags: [postgresql, api, crm-core, sprint1]
---

# TASK-001：CRM核心业务CRUD API

## 需求描述
实现招投标管理、项目制管理、组织层级管理的完整CRUD API。

## 技术规范
- 数据库：PostgreSQL 15+ + PGVector
- 认证：JWT Bearer Token（先实现端点逻辑，认证中间件后续添加）
- 响应格式：{ code, message, data }

## API端点

### 招投标管理 (/api/v1/bidding)
- POST   /                     创建投标项目
- GET    /                     投标列表(分页+筛选)
- GET    /{id}                 投标详情
- PUT    /{id}                 更新投标状态(9态状态机)
- GET    /calendar             投标日历

### 项目管理 (/api/v1/projects)
- POST   /                     创建项目
- GET    /                     项目列表(分页+看板)
- GET    /{id}                 项目详情
- PUT    /{id}/stage           推进阶段(12阶段流转)
- GET    /kanban               看板视图

### 组织层级 (/api/v1/organizations)
- POST   /                     创建组织节点
- GET    /tree                 组织树
- PUT    /{id}                 更新组织
- DELETE /{id}                 删除组织

## 验收标准
- [ ] 所有端点返回标准JSON格式
- [ ] 分页参数(page, page_size)，默认page=1, size=20
- [ ] 排序支持created_at DESC/ASC
- [ ] 参数校验完整（Pydantic/JSR303）
- [ ] 单元测试覆盖率 > 80%
- [ ] API文档自动生成（Swagger/OpenAPI）

## 完成标记
完成后将本文件移至 tasks/done/ 并创建 TASK-001-done.md
