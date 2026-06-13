---
task_id: TASK-024
title: Sprint6 QA — 全量回归 + 性能终测 + 部署验证
assignee: pc5
role: qa-engineer
priority: P1
deadline: 2026-06-17
branch: feature/TASK-024-final-qa
dependencies: [TASK-020, TASK-021, TASK-022]
tags: [sprint6, qa, regression, release]
---

# TASK-024：Sprint6 终测QA

## Part A: 全量回归
- 运行全部 120+ 测试用例
- 输出回归报告
- 失败用例清零

## Part B: 性能终测
- 全API端点性能基线
- P95 < 200ms (CRUD), P95 < 3s (AI)
- locust 并发500用户压测

## Part C: 部署验证
- Docker Compose 一键启动验证
- 健康检查端点验证

## 验收标准
- [ ] 全量回归通过率 > 98%
- [ ] 性能基线达标
- [ ] Docker部署验证通过
- [ ] QA签认报告

完成后: git commit, 移至 tasks/done/
