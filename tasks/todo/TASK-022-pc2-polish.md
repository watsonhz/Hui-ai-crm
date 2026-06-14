---
task_id: TASK-022
title: PC2 前端打磨 — 响应式+无障碍+性能
assignee: pc2
role: pm-frontend
priority: P1
deadline: 2026-06-21
branch: feature/TASK-022-polish
dependencies: [TASK-002, TASK-006, TASK-010, TASK-014, TASK-018]
tags: [final, polish, frontend]
---

# TASK-022：前端打磨

## 范围
1. 移动端响应式适配（320px-1920px）
2. 无障碍（ARIA label, focus管理）
3. 打包优化（lazy loading, code splitting）
4. 统一错误页面（404/403/500）
5. 暗色模式支持

## 验收
- [ ] Lighthouse > 90
- [ ] 所有页面移动端可用
- [ ] npm audit 0 高危
