---
task_id: TASK-018
title: PC2 关系图谱+诊断页面
assignee: pc2
role: pm-frontend
priority: P0
deadline: 2026-06-19
branch: feature/TASK-018-graph-diagnosis
dependencies: [TASK-002]
tags: [sprint5, frontend, vue, graph]
---

# TASK-018：关系图谱+诊断页面

## 需求
客户关系知识图谱可视化 + AI诊断结果展示。

## 页面
- /graph — 关系图谱（节点+边，ECharts/D3）
- /diagnosis — AI诊断结果（流失预测+评分）

## 安全要求
- [ ] 图谱节点 label/tooltip 全转义（防 XSS via 数据注入）
- [ ] AI诊断结果不渲染为 HTML
- [ ] 图谱数据按用户权限过滤
