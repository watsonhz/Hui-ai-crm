---
task_id: TASK-025
title: PostgreSQL数据库迁移 + 真实数据模型 + Redis缓存
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-25
branch: feature/TASK-025-postgresql
dependencies: [TASK-023]
tags: [sprint7, postgresql, redis, alembic, migration]
---

# TASK-025：PostgreSQL迁移 + Redis缓存

## 需求描述
从 SQLite 开发环境迁移至 PostgreSQL 15+ 生产环境，接入 Redis 缓存层。

## Part A: PostgreSQL 迁移
- Docker Compose 启动 PostgreSQL 15 + Redis 7
- Alembic 初始化迁移脚本（替代 init_db.py）
- 所有模型添加索引优化
- PGVector 扩展启用（为 AI 向量检索做准备）

## Part B: Redis 缓存
- 客户列表缓存（TTL 5分钟）
- 组织树缓存
- Token 黑名单（登出后失效）

## Part C: 数据模型扩展
- 客户表增加字段：scale, annual_revenue, tags
- 投标表：competitor_info JSON 字段
- 项目表：milestones JSON 字段

## 验收标准
- PostgreSQL 迁移成功，Alembic upgrade 无报错
- Redis 缓存命中率 > 60%
- 76 测试全部通过
- 查询性能提升 > 30%

完成后: git commit/push, 移至 tasks/done/
