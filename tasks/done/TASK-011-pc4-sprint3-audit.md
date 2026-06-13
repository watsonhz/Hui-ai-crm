---
task_id: TASK-011
title: Sprint3 安全审计 — AI报告+知识库+合同验收
assignee: pc4
role: security-auditor
priority: P1
deadline: 2026-06-15
branch: feature/TASK-011-sprint3-audit
dependencies: [TASK-007, TASK-009, TASK-010]
tags: [sprint3, security, cso]
---

# TASK-011：Sprint3 安全审计

## 审计范围
- backend/app/services/report_generator.py — AI报告生成
- backend/app/services/vector_service.py — RAG向量检索
- backend/app/api/v1/ai/reports.py — 报告API
- backend/app/api/v1/knowledge.py — 知识库API
- frontend/src/views/contracts/ — 合同页面
- frontend/src/views/acceptance/ — 验收页面

## 重点检查
1. AI 报告注入风险（Prompt Injection）
2. 向量检索数据泄露
3. 合同金额篡改风险 (支付安全)
4. 文件上传安全
5. 新 API 认证授权

## 验收标准
- [ ] bandit + safety 扫描通过
- [ ] 审计报告输出 SEC-AUDIT-20260615-SPRINT3.md
- [ ] 发现 ≥ 0 个安全问题（含已修复）

完成后: git commit/push, 移至 tasks/done/
