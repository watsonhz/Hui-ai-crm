---
task_id: TASK-005
title: PC3 决策链API — 销售阶段流转+审批
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-16
branch: feature/TASK-005-decision-chain
dependencies: [TASK-001]
tags: [sprint3, api, decision-chain, postgresql]
---

# TASK-005：决策链API

## 需求
实现销售决策链（线索→商机→需求→方案→报价→谈判→合同→交付→验收→回款→运维→结项）的阶段流转 API。

## 端点
- POST /api/v1/decision-chain/advance — 推进阶段
- GET  /api/v1/decision-chain/{project_id} — 查决策链状态
- GET  /api/v1/decision-chain/history/{project_id} — 阶段历史

## 验收
- [ ] 12阶段状态机校验
- [ ] 阶段变更记录审计日志
- [ ] 非当前负责人不可推进
- [ ] pytest > 80% 覆盖
