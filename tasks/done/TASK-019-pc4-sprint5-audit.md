---
task_id: TASK-019
title: Sprint5 安全审计 — AI销售+营销+RBAC权限+图谱XSS
assignee: pc4
role: security-auditor
priority: P1
deadline: 2026-06-17
branch: feature/TASK-019-sprint5-audit
dependencies: [TASK-015, TASK-017, TASK-018]
tags: [sprint5, security, cso, rbac, ai]
---

# TASK-019：Sprint5 安全审计

## 审计范围
- AI销售: 线索评分/流失预测逻辑安全
- AI营销: 内容生成注入风险
- RBAC: 权限越权测试/角色提权
- 图谱: XSS via节点数据注入
- 操作日志: 日志完整性+防篡改

## 验收标准
- [ ] bandit + safety 扫描通过
- [ ] RBAC 越权测试
- [ ] 审计报告 SEC-AUDIT-20260617-SPRINT5.md

完成后: git commit, 移至 tasks/done/
