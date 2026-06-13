---
task_id: TASK-005
title: P1修复 + 决策链图谱API + AI诊断引擎
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-14
branch: feature/TASK-005-decision-chain
dependencies: [TASK-001]
tags: [sprint2, decision-chain, ai, security-fix]
---

# TASK-005：P1修复 + 决策链图谱API + AI诊断引擎

## Part A: P1 安全修复
修复 PC4 审计发现的 P1-001：`backend/app/core/config.py` 中 DATABASE_URL 拆分
为独立环境变量 (DB_HOST/DB_PORT/DB_USER/DB_PASS/DB_NAME)

## Part B: 决策链图谱 API (/api/v1/decision-chain)
- POST /                     创建决策链节点
- GET /{customer_id}/graph   获取决策链图谱数据
- PUT /{node_id}             更新节点（角色/权重/支持度）
- GET /{customer_id}/gap     检测决策链缺口

节点属性：name, role(8种), weight(1-10), support_level, contact_frequency, org_unit

## Part C: AI诊断信号引擎骨架
- backend/services/diagnosis_engine.py
- 实现 S1-S4 时间维度信号（拜访超期/阶段卡顿/间隔拉长/待办逾期）
- 每个信号 calculate() 返回 {triggered, severity, diagnosis, advice}

## 验收标准
- [ ] P1-001 已修复，通过安全复查
- [ ] 决策链 4 端点可用
- [ ] AI诊断 4 信号可计算
- [ ] pytest 测试 > 80% 覆盖

## 完成后
git commit/push，移动本文件至 tasks/done/
