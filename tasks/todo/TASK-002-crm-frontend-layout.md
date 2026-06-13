---
task_id: TASK-002
title: CRM 管理后台主布局 + 路由
assignee: pc2
role: frontend-developer
priority: P0 (最高)
deadline: 2026-06-09
branch: feat/TASK-002-frontend-layout
dependencies: []
tags: [react, typescript, mui, crm-core]
---

# TASK-002：CRM 管理后台主布局 + 路由

## 需求描述
搭建 CRM 管理后台的框架布局和路由系统。

## 技术规范
- 框架：React 18 + TypeScript + React Router 6
- UI 库：MUI (Material-UI) 5
- 文件位置：frontend/src/

## 页面结构
- /                 → 重定向到 /dashboard
- /dashboard        → 数据仪表盘（首页）
- /customers        → 客户列表页
- /customers/:id    → 客户详情页
- /customers/new    → 新建客户页
- /funnel           → 销售漏斗页
- /analytics        → 数据分析页
- /settings         → 系统设置页

## 布局要求
- 左侧可折叠导航菜单（含图标）
- 顶部导航栏（用户信息、通知、退出）
- 面包屑导航
- 响应式设计（支持 1920px ~ 1366px）

## 验收标准
- [ ] 所有路由正常工作
- [ ] 侧边栏可折叠
- [ ] 面包屑自动生成
- [ ] 404 页面
- [ ] 加载状态和错误边界
