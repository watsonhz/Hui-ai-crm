---
task_id: TASK-010
title: PC2 合同管理+验收页面
assignee: pc2
role: pm-frontend
priority: P0
deadline: 2026-06-17
branch: feature/TASK-010-contract-acceptance
dependencies: [TASK-002]
tags: [sprint3, frontend, vue, contract]
---

# TASK-010：合同管理+验收页面

## 需求
合同列表、详情、金额展示 + 验收管理三状态面板。

## 页面
- /contracts — 合同列表（金额用 Decimal，非 float）
- /contracts/:id — 合同详情
- /acceptance — 验收管理（待验收/已通过/已驳回）

## 安全要求
- [ ] 金额字段不可前端篡改（后端二次校验）
- [ ] 验收驳回理由 XSS 防护（escapeHtml）
- [ ] 禁止 dangerouslyUseHTMLString 未转义
- [ ] 合同签字确认有二次弹窗
