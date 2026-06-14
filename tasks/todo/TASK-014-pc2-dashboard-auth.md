---
task_id: TASK-014
title: PC2 驾驶舱+登录页面
assignee: pc2
role: pm-frontend
priority: P0
deadline: 2026-06-18
branch: feature/TASK-014-dashboard-auth
dependencies: [TASK-002]
tags: [sprint4, frontend, vue, dashboard, auth]
---

# TASK-014：驾驶舱+登录页面

## 需求
数据驾驶舱看板 + 登录/注册页面。

## 页面
- /login — 登录页（验证码+错误次数提示）
- /dashboard — 驾驶舱（ECharts 图表+统计卡片）

## 安全要求
- [ ] ECharts 数据全部转义（无用户数据直入 option）
- [ ] 登录页 5 次失败锁定提示
- [ ] 图表 API 按用户权限过滤数据
- [ ] Token 存储 httpOnly cookie（非 localStorage）
