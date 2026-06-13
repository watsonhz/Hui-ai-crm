---
task_id: TASK-010
title: 合同管理 + 验收管理 + LTC全链路页面
assignee: pc2
role: frontend-developer
priority: P0
deadline: 2026-06-15
branch: feature/TASK-010-contract-acceptance
dependencies: [TASK-006]
tags: [sprint3, vue3, contract, acceptance, ltc]
---

# TASK-010：合同管理 + 验收管理 + LTC全链路页面

## 合同管理页面 (/contracts)
- 合同列表 (分页+筛选+搜索)
- 合同详情 (含交付阶段时间线)
- 合同审批状态流 (Flowable BPM 驱动)
- 回款计划 + 实际回款记录

## 验收管理页面 (/acceptance)
- 分阶段验收列表
- 验收详情 (验收项+标准+结果)
- 验收报告上传
- 回款关联

## LTC全链路看板 (/ltc)
- 项目全生命周期时间线
- 阶段流转可视化
- 卡顿预警 (AI诊断信号联动)

## 组件
- ContractTimeline.vue — 合同交付阶段时间线
- AcceptanceForm.vue — 验收表单
- LTCDashboard.vue — LTC全链路看板

## 验收标准
- [ ] 合同 CRUD 页面可用
- [ ] 验收流程可走通
- [ ] LTC 看板可视化正确
- [ ] API 联调通过

完成后: git commit/push, 移至 tasks/done/
