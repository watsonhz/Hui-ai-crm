---
task_id: TASK-006
title: 5次拜访三屏交互组件（核心页面）
assignee: pc2
role: frontend-developer
priority: P0
deadline: 2026-06-14
branch: feature/TASK-006-visit-flow
dependencies: [TASK-002]
tags: [sprint2, vue3, visit-flow, core-feature]
---

# TASK-006：5次拜访三屏交互组件

## 屏1 - 拜访准备卡 (VisitPrepare.vue)
- 顶部：拜访阶段标签 + 客户名称
- 告警区(红/橙色)：AI信号触发（关键人超期/决策链缺口/P0待办逾期）
- 核心信息5行：时间/地点/我方参会人/客户方参会人/拜访目标
- 上次待办自动带入（未完成 actionItems）
- 建议议题(可编辑)：AI推荐的议题清单
- 可展开详情：完整客户背景/决策链/历史拜访

## 屏2 - 拜访快速记录 (VisitRecord.vue)
- 语音模式：录音→转文字→实时显示
- 手动模式：议题结果勾选（通过/部分/未达成）
- 客户表态（积极/观望/抵触）+ 关系温度（升温/稳定/降温）

## 屏3 - AI拜访纪要 (VisitSummary.vue)
- 左栏：AI生成纪要(可编辑) — 摘要/关键决策/客户关注点
- 右栏：AI行动项 — 负责人/截止日期/优先级
- 一键预约下次拜访按钮

## 数据流
- Pinia store: useVisitStore
- API: GET /api/v1/relationships/{customerId}/visits

## 验收标准
- [ ] 三屏流程完整可走通
- [ ] 屏1→屏2→屏3 状态传递正确
- [ ] 响应式设计 (1920px~1366px)

## 完成后
git commit/push，移动本文件至 tasks/done/
