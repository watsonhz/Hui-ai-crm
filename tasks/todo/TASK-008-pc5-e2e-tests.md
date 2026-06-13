---
task_id: TASK-008
title: E2E测试 + 性能基线 + 扩展API测试
assignee: pc5
role: qa-engineer
priority: P1
deadline: 2026-06-14
branch: feature/TASK-008-e2e-tests
dependencies: [TASK-004, TASK-005, TASK-006]
tags: [sprint2, e2e, performance, qa]
---

# TASK-008：E2E测试 + 性能基线

## Part A: E2E 测试 (Playwright)
- tests/e2e/test_visit_flow.spec.ts — 5次拜访三屏流程
- tests/e2e/test_bidding_flow.spec.ts — 招投标全流程
- tests/e2e/test_decision_chain.spec.ts — 决策链操作

## Part B: 扩展 API 测试
- tests/api/test_decision_chain.py — 决策链4端点
- tests/api/test_diagnosis.py — AI诊断信号

## Part C: 性能基线
- 运行 locust 建立 Sprint2 性能基准
- 输出 tests/reports/performance-baseline-sprint2.html

## 验收标准
- [ ] 3 个 E2E 测试通过
- [ ] 新 API 测试覆盖 > 80%
- [ ] 性能基线报告生成

## 完成后
git commit/push，移动本文件至 tasks/done/
