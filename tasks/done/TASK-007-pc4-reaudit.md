---
task_id: TASK-007
title: Sprint2 安全再审计 — P0验证 + 决策链API审查
assignee: pc4
role: security-auditor
priority: P1
deadline: 2026-06-14
branch: feature/TASK-007-reaudit
dependencies: [TASK-003, TASK-005]
tags: [sprint2, security, cso]
---

# TASK-007：Sprint2 安全再审计

## 任务
1. 验证 P0-001 (SECRET_KEY) 已修复
2. 验证 P1-001 (DB凭据) 已修复
3. 对新代码 TASK-005/006 执行 /cso 审计
4. 更新安全基线报告

## 审计范围
- backend/app/core/config.py (P0/P1 修复验证)
- backend/app/api/v1/decision_chain.py (新API)
- backend/services/diagnosis_engine.py (AI引擎)
- frontend/src/components/relationships/ (拜访组件)

## 验收标准
- [ ] P0/P1 修复确认通过
- [ ] 新代码安全审查完成
- [ ] 签认报告输出至 security/audit-reports/SEC-AUDIT-20260614-SPRINT2.md

## 完成后
git commit/push，移动本文件至 tasks/done/
