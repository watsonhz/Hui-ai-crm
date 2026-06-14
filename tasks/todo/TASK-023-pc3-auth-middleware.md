---
task_id: TASK-023
title: JWT认证中间件 + 安全加固 + CI/CD流水线
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-21
branch: feature/TASK-023-auth-security
dependencies: [TASK-001, TASK-003]
tags: [sprint6, auth, security, jwt, ci-cd]
---

# TASK-023：JWT认证中间件 + 安全加固 + CI/CD流水线

## 需求描述
实现 PC4 安全审查报告中标记的 HIGH 优先级项目，完成认证中间件和 CI/CD 流水线。

## Part A: JWT 认证中间件
- 实现 JWT Bearer Token 认证中间件（app/core/auth.py）
- POST /api/v1/auth/login → 返回 JWT token
- POST /api/v1/auth/refresh → 刷新 token
- 所有业务端点添加 Depends(get_current_user)
- Token 过期自动返回 401

## Part B: 安全加固（PC4 HIGH项目）
- SECRET_KEY 改为从环境变量读取，无默认值
- CORS origins 改为环境变量配置
- 添加速率限制（slowapi，60次/分钟/IP）
- 添加安全响应头中间件
- LIKE 查询参数转义（% 和 _）

## Part C: CI/CD 流水线
- .github/workflows/ci.yml — lint + test + build
- backend/tests/ 集成到 CI
- PC5 自托管 Runner 配置
- 部署到开发环境的 Docker Compose

## 技术规范
- JWT: python-jose + passlib
- 速率限制: slowapi
- 安全头: starlette.middleware
- CI: GitHub Actions

## 验收标准
- [ ] 未登录访问 API 返回 401
- [ ] 登录后访问 API 正常
- [ ] 速率限制生效（60次/分钟后返回 429）
- [ ] 安全头在所有响应中存在
- [ ] CI 流水线可运行
- [ ] 测试覆盖率 > 80%

完成后: git commit/push, 移至 tasks/done/
