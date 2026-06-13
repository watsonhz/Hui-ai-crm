---
task_id: TASK-015
title: Sprint4 安全审计 — BPM流程注入 + 登录安全 + 图表XSS
assignee: pc4
role: security-auditor
priority: P1
deadline: 2026-06-16
branch: feature/TASK-015-sprint4-audit
dependencies: [TASK-011, TASK-013, TASK-014]
tags: [sprint4, security, cso, auth, bpm]
---

# TASK-015：Sprint4 安全审计

## 审计范围

### BPM 工作流
- 流程定义注入 (XXE/BPMN XML注入)
- 审批权限校验 (越权审批)
- 流程变量泄露

### 登录认证
- JWT Token 刷新/撤销机制
- 暴力破解防护 (登录失败锁定)
- 短信验证码防刷
- 微信 OAuth state 参数防 CSRF

### 图表安全
- ECharts 数据注入 (用户数据→图表渲染 XSS)
- 驾驶舱数据权限 (跨用户数据泄露)

## 验收标准
- [ ] bandit + safety 扫描通过
- [ ] 登录攻击场景测试
- [ ] 审计报告 SEC-AUDIT-20260616-SPRINT4.md

完成后: git commit/push, 移至 tasks/done/
