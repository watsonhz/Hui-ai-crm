---
task_id: TASK-013
title: AI客户服务(工单+SLA) + Flowable BPM工作流集成
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-16
branch: feature/TASK-013-ai-service-bpm
dependencies: [TASK-009]
tags: [sprint4, ai-service, bpm, flowable, workflow]
---

# TASK-013：AI客户服务 + BPM工作流集成

## Part A: AI客户服务 (工单+SLA)
文件: backend/app/services/ai_service.py, backend/app/api/v1/ai/service.py

工单管理:
- POST /api/v1/ai/service/tickets — 创建工单
- GET  /api/v1/ai/service/tickets — 工单列表(分页+状态筛选)
- PUT  /api/v1/ai/service/tickets/{id} — 更新工单/分配/SLA

SLA 规则引擎:
- 根据客户等级(战略/重点/普通)自动计算响应时间和解决时间
- 超时自动告警 (S13-S14 信号)

## Part B: Flowable BPM 工作流集成
文件: backend/app/services/workflow_service.py

- 审批流: 合同审批/验收审批/变更审批
- 拜访阶段流转: 5次拜访标准化流程
- BPMN 流程定义: 3个核心流程模板

## 验收标准
- [ ] 工单 CRUD 端点可用
- [ ] SLA 规则按客户等级正确计算
- [ ] 3 个 BPMN 流程定义就绪
- [ ] 审批流 API 可触发

完成后: git commit/push, 移至 tasks/done/
