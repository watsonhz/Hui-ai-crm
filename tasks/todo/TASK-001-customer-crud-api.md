---
task_id: TASK-001
title: CRM 客户管理 CRUD API
assignee: pc3
role: backend-architect
priority: P0 (最高)
deadline: 2026-06-09
branch: feat/TASK-001-customer-crud
dependencies: []
tags: [python, fastapi, mysql, crm-core]
---

# TASK-001：客户管理 CRUD API

## 需求描述
实现 CRM 系统核心的客户增删改查 API。

## 技术规范
- 框架：FastAPI + SQLAlchemy 2.0 + Pydantic v2
- 数据库：MySQL 8.0（参考 docs/architecture/database-er.md）
- 文件位置：backend/api/customers.py, backend/models/customer.py
- 认证：JWT Bearer Token（先实现端点逻辑，认证中间件后续添加）

## API 端点
POST   /api/v1/customers/         - 创建客户
GET    /api/v1/customers/         - 客户列表（分页+筛选）
GET    /api/v1/customers/{id}     - 客户详情
PUT    /api/v1/customers/{id}     - 更新客户
DELETE /api/v1/customers/{id}     - 软删除客户

## 验收标准
- [ ] 所有端点返回标准 JSON：{ code, message, data }
- [ ] 分页参数：page, page_size，默认 page=1, page_size=20
- [ ] 筛选支持：name, company, status, level, source
- [ ] 排序支持：created_at DESC/ASC
- [ ] 参数校验：必填字段、邮箱格式、手机号格式
- [ ] 单元测试覆盖率 > 80%
- [ ] Swagger 文档自动生成

## 完成标记
完成后将本文件移至 tasks/done/ 并创建 TASK-001-done.md
