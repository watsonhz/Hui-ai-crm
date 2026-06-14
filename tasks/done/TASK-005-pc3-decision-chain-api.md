---
task_id: TASK-005
<<<<<<< HEAD
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
=======
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
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
