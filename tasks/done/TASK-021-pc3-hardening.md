---
task_id: TASK-021
title: PC3 系统加固 — 性能+安全+文档
assignee: pc3
role: backend-architect
priority: P1
deadline: 2026-06-21
branch: feature/TASK-021-hardening
dependencies: [TASK-001, TASK-005, TASK-009, TASK-013, TASK-017]
tags: [final, hardening, docs]
---

# TASK-021：系统加固

## 范围
1. DB 索引优化（慢查询 < 100ms）
2. Redis 缓存层（热门数据 TTL 5min）
3. API 文档补全（OpenAPI description）
4. 错误处理统一（无 stack trace 泄露）
5. 全量 bandit+safety 扫描 0 告警

## 验收
- [ ] 所有端点 response time P95 < 500ms
- [ ] 错误响应不含内部堆栈
- [ ] Swagger 文档完整可读
