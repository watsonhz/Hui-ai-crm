---
task_id: TASK-012
title: Sprint3 QA — AI功能测试 + 合同验收E2E + 性能压测
assignee: pc5
role: qa-engineer
priority: P1
deadline: 2026-06-15
branch: feature/TASK-012-sprint3-qa
dependencies: [TASK-008, TASK-009, TASK-010]
tags: [sprint3, qa, e2e, performance]
---

# TASK-012：Sprint3 QA 测试

## Part A: AI 功能测试
- tests/api/test_ai_reports.py — 日报/周报/月报生成
- tests/api/test_knowledge.py — 文档上传+语义搜索
- tests/api/test_diagnosis_engine.py — S5-S12 信号扩展

## Part B: 合同验收 E2E
- tests/e2e/test_contract_flow.spec.ts — 合同创建→审批→回款
- tests/e2e/test_acceptance_flow.spec.ts — 分阶段验收流程

## Part C: 性能压测
- 对 AI 报告生成接口做并发测试 (locust)
- 对 PGVector 搜索做延迟基线
- 输出 tests/reports/performance-sprint3.html

## 验收标准
- [ ] 新 API 测试覆盖 > 80%
- [ ] 2 个 E2E 流程通过
- [ ] 性能基线报告生成
- [ ] P95 < 3s (AI接口), P95 < 500ms (CRUD接口)

完成后: git commit/push, 移至 tasks/done/
