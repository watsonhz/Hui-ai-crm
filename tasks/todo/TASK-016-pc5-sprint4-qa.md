---
task_id: TASK-016
title: Sprint4 QA — 工单SLA测试 + 认证流程E2E + BPM流程测试
assignee: pc5
role: qa-engineer
priority: P1
deadline: 2026-06-16
branch: feature/TASK-016-sprint4-qa
dependencies: [TASK-012, TASK-013, TASK-014]
tags: [sprint4, qa, e2e, auth-testing]
---

# TASK-016：Sprint4 QA 测试

## Part A: API 测试
- tests/api/test_ai_service.py — 工单 CRUD + SLA 规则验证
- tests/api/test_workflow.py — BPM 审批流触发+状态流转

## Part B: 登录认证 E2E
- tests/e2e/test_login_flow.spec.ts — 密码登录/微信扫码/短信验证
- tests/e2e/test_auth_guard.spec.ts — 未登录拦截/Token过期

## Part C: 性能压测
- locust: 并发登录 (100用户)
- locust: 工单创建+查询混合负载
- 输出 tests/reports/performance-sprint4.html

## 验收标准
- [ ] 工单 API 测试覆盖 > 80%
- [ ] BPM 审批流测试覆盖
- [ ] 2 个登录 E2E 通过
- [ ] 性能基线 P95 < 500ms (登录), P95 < 1s (工单)

完成后: git commit/push, 移至 tasks/done/
