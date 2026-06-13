---
task_id: TASK-021
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
