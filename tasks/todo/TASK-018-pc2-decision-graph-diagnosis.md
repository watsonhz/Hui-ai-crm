---
task_id: TASK-018
title: 决策链图谱可视化 + AI诊断面板 + 系统管理页面
assignee: pc2
role: frontend-developer
priority: P0
deadline: 2026-06-17
branch: feature/TASK-018-decision-diagnosis
dependencies: [TASK-014]
tags: [sprint5, vue3, echarts, graph, diagnosis, admin]
---

# TASK-018：决策链图谱 + AI诊断面板 + 系统管理

## Part A: 决策链图谱可视化 (DecisionChainGraph.vue)
- ECharts 力导向图/关系图
- 节点按8种角色分类着色(8色)
- 节点大小反映影响力权重(1-10)
- 边的粗细反映关系亲密度
- 支持拖拽+缩放+点击展开详情卡片
- 三种视图切换：点·关键关系 / 面·普遍关系 / 势·组织关系

## Part B: AI诊断面板 (DiagnosisPanel.vue)
- 6个板块: 客户全景/问题诊断/行动建议/风险预警/建议话术/一键生成准备卡
- 诊断信号颜色区分(红/黄/蓝)
- 每条诊断标注数据依据+日期
- 话术按目标角色分组

## Part C: 系统管理页面 (/settings 扩展)
- 用户管理表格+编辑Dialog
- 角色权限矩阵
- 操作日志时间线

## 验收标准
- [ ] 决策链图谱正确渲染
- [ ] AI诊断6板块完整
- [ ] 系统管理3页面可用
- [ ] 响应式适配

完成后: git commit, 移至 tasks/done/
