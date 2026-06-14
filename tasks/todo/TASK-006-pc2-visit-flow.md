---
task_id: TASK-006
title: PC2 客户拜访流程页面 — 准备卡+记录+AI纪要
assignee: pc2
role: pm-frontend
priority: P0
deadline: 2026-06-16
branch: feature/TASK-006-visit-flow
dependencies: [TASK-002]
tags: [sprint3, frontend, vue, visit]
---

# TASK-006：客户拜访流程页面

## 需求
实现拜访三屏流程：准备卡 → 快速记录 → AI纪要。

## 页面
- /visit/prep — 拜访准备卡（客户信息+告警+议题）
- /visit/record — 快速记录（语音+手动勾选）
- /visit/minutes — AI纪要（生成+编辑+行动项）

## 验收
- [ ] 三屏切换流畅，数据跨屏共享
- [ ] 语音模拟可用
- [ ] AI纪要为可编辑文本框
- [ ] 无 XSS（禁止 v-html/dangerouslyUseHTMLString）
