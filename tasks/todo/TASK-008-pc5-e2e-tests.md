---
task_id: TASK-008
title: PC5 Sprint3 E2E+性能测试
assignee: pc5
role: qa-engineer
priority: P0
deadline: 2026-06-17
branch: feature/TASK-008-e2e-tests
dependencies: [TASK-005, TASK-006, TASK-009, TASK-010]
tags: [sprint3, qa, e2e, playwright]
---

# TASK-008：Sprint3 QA测试

## 范围
- 决策链 API 功能正确性
- 拜访流程 E2E (Playwright)
- AI报告生成性能 (k6)
- 知识库搜索准确率

## 验收
- [ ] Playwright E2E: 拜访三屏流程
- [ ] k6: /ai/reports/generate P95<3s
- [ ] API: 所有 Sprint3 端点 200 响应
- [ ] 0 P0/P1 Bug
