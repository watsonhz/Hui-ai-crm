---
task_id: TASK-021
<<<<<<< HEAD
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
=======
title: Rate Limiting + CORS收紧 + 全API认证加固
assignee: pc3
role: backend-architect
priority: P1
deadline: 2026-06-17
branch: feature/TASK-021-hardening
dependencies: [TASK-017]
tags: [sprint6, security, rate-limit, cors, hardening]
---

# TASK-021：Rate Limiting + 安全加固

## Part A: Rate Limiting (P2修复)
- 全API端点添加速率限制中间件
- 登录接口: 5次/分钟/IP
- AI接口: 30次/分钟/用户
- CRUD接口: 120次/分钟/用户
- 429响应 + Retry-After头

## Part B: CORS 收紧 (P2修复)
- allow_origins 限制为内网IP白名单
- allow_methods 限制为实际使用的HTTP方法
- allow_headers 限制为必要请求头

## Part C: 认证加固
- 所有端点添加 Depends(get_current_user)
- Token刷新端点
- 登录失败锁定机制

## 验收标准
- [ ] Rate Limiting生效
- [ ] CORS白名单限制
- [ ] 全端点认证覆盖
- [ ] pytest测试

完成后: git commit, 移至 tasks/done/
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
