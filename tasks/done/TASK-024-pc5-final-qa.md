---
task_id: TASK-024
title: 全量回归 + 性能终测 + Docker验证
assignee: pc5
role: qa-engineer
priority: P0
deadline: 2026-06-15
branch: feature/TASK-024-final-qa
dependencies: [TASK-020]
tags: [final, qa, docker, performance, regression]
---

# TASK-024：最终 QA 验证

## Part A: Docker 验证
- 创建 backend/Dockerfile + frontend/Dockerfile
- 更新 docker-compose.yml 加入 app 服务
- 验证 docker-compose config 有效

## Part B: 全量回归
- 运行全部 142+ API 测试
- 运行全部 61+ E2E 测试
- 输出 tests/reports/regression-final.html

## Part C: 性能终测
- locust 100 并发 180s 全量压测
- 输出 tests/reports/performance-final.html

## 验收标准
- [ ] Docker Compose 配置完整（MySQL+Redis+Backend+Frontend）
- [ ] 全量回归通过率 > 95%
- [ ] 性能终测 P95 < 500ms (CRUD), P95 < 3s (AI)

完成后: git commit, 移至 tasks/done/
