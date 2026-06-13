---
task_id: TASK-014
title: 运营数据驾驶舱(ECharts) + 微信/短信登录认证页面
assignee: pc2
role: frontend-developer
priority: P0
deadline: 2026-06-16
branch: feature/TASK-014-dashboard-auth
dependencies: [TASK-010]
tags: [sprint4, vue3, echarts, dashboard, auth]
---

# TASK-014：运营驾驶舱 + 登录认证页面

## Part A: 运营数据驾驶舱 (ECharts)
增强 DashboardPage.vue:

图表:
- 销售漏斗图 (funnel) — 商机→投标→中标转化
- 业绩趋势图 (line) — 月度合同额/回款额
- 客户分布图 (pie) — 按行业/区域/等级
- 项目看板概览 (gauge) — 进行中/卡顿/逾期
- AI诊断信号汇总 (heatmap)

## Part B: 登录认证页面
文件: frontend/src/views/login/LoginPage.vue

- 密码登录 (用户名+密码 → JWT)
- 微信扫码登录 (二维码展示)
- 短信验证码登录 (手机号+验证码+倒计时)
- 记住我 + 忘记密码链接

## Part C: 路由守卫
- router/authGuard.ts — 未登录跳转 /login
- Token 过期自动刷新

## 验收标准
- [ ] 5 种 ECharts 图表正确渲染
- [ ] 3 种登录方式 UI 完成
- [ ] 路由守卫生效 (未登录→/login)
- [ ] 响应式适配

完成后: git commit/push, 移至 tasks/done/
