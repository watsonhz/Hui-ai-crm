---
task_id: TASK-024
title: PC5 终测签署 — 全量回归+性能+安全
assignee: pc5
role: qa-engineer
priority: P0
deadline: 2026-06-22
branch: feature/TASK-024-final-qa
dependencies: [TASK-021, TASK-022, TASK-023]
tags: [final, qa, release]
---

# TASK-024：终测签署

## 范围
1. 全量回归（所有 36 端点 + 前端所有页面）
2. 性能基准（k6: 100并发 30s）
3. 安全终验（OWASP Top 10 全项）
4. 跨浏览器（Edge + Chrome）

## 验收
- [ ] 211 pytest + E2E 全绿
- [ ] k6 P95 < 1s, 0 errors
- [ ] 4 浏览器截图一致
- [ ] 签署发布令 → PC1 审批上线
