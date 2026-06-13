---
task_id: TASK-002
title: CRM管理后台主布局 + 路由 + 5次拜访页面
assignee: pc2
role: frontend-developer
priority: P0 (最高)
deadline: 2026-06-20
branch: feature/TASK-002-frontend-layout
dependencies: []
tags: [vue3, typescript, crm-core, sprint1]
---

# TASK-002：CRM管理后台主布局 + 路由 + 5次拜访页面

## 需求描述
搭建CRM管理后台的框架布局、路由系统，以及5次标准化拜访的三屏页面。

## 技术规范
- 框架：Vue3 + TypeScript + Vue Router 4
- UI库：Element Plus（PC1已确认）
- 图表：ECharts 5
- 文件位置：frontend/src/

## 页面结构
- /                    重定向 /dashboard
- /dashboard           运营数据驾驶舱
- /customers           客户列表（含组织树+三级分层）
- /customers/:id       客户详情（含AI诊断面板+决策链图谱）
- /bidding             招投标管理（9态看板）
- /projects            项目管理（12阶段看板，支持拖拽）
- /relationships       关系维护（5次拜访三屏流程）
- /acceptance          验收管理
- /ai-reports          工作总结（日报/周报/月报）
- /knowledge           知识库管理
- /settings            系统设置

## 5次拜访三屏页面（核心页面）
- 屏1-准备卡：告警区+核心信息+上次待办+建议议题+可展开详情
- 屏2-快速记录：语音模式+手动勾选模式
- 屏3-AI纪要：左栏纪要(可编辑)+右栏行动项

## 验收标准
- [ ] 所有路由正常工作
- [ ] 侧边栏可折叠，含菜单图标
- [ ] 面包屑自动生成
- [ ] 404页面
- [ ] 响应式设计（1920px~1366px）
- [ ] 5次拜访三屏流程可走通

## 完成标记
完成后将本文件移至 tasks/done/ 并创建 TASK-002-done.md
