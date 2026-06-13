---
task_id: TASK-020
title: Sprint5 QA — AI销售测试+RBAC权限测试+全量回归
assignee: pc5
role: qa-engineer
priority: P1
deadline: 2026-06-17
branch: feature/TASK-020-sprint5-qa
dependencies: [TASK-016, TASK-017, TASK-018]
tags: [sprint5, qa, regression, rbac]
---

# TASK-020：Sprint5 QA

## Part A: API 测试
- tests/api/test_ai_sales.py — 线索评分+流失预测+交叉销售
- tests/api/test_ai_marketing.py — 营销推荐+内容生成
- tests/api/test_system_rbac.py — 用户/角色/权限 CRUD + 越权验证

## Part B: E2E 测试
- tests/e2e/test_decision_graph.spec.ts — 图谱交互
- tests/e2e/test_admin_rbac.spec.ts — 管理员操作

## Part C: 全量回归
- 运行全部 100+ 测试用例
- 输出 tests/reports/regression-sprint5.html

## 验收标准
- [ ] 新 API 测试覆盖 > 80%
- [ ] 全量回归通过率 > 95%
- [ ] RBAC 越权测试通过

完成后: git commit, 移至 tasks/done/
