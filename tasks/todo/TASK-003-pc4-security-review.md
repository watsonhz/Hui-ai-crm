---
task_id: TASK-003
title: PC4 安全审查基础设施 + 对抗性代码审查
assignee: pc4
role: security-reviewer
priority: P0 (最高)
deadline: 2026-06-10
branch: feat/TASK-003-security-review
dependencies: [TASK-001]
tags: [security, adversarial-review, owasp, code-review]
---

# TASK-003：PC4 安全审查基础设施 + 对抗性代码审查

## 需求描述
PC4 作为安全审查闸门（v3.1.0 第一闸），对 PC3 提交的所有 L4+ 代码进行安全审查和对抗性验证。

## 审查范围（按 v3.1.0 6.5 节）
- SQL 注入 / XSS / CSRF / 越权访问
- 支付金额篡改风险
- 密钥泄露 / 敏感数据加密
- OWASP Top 10 全覆盖

## 技术规范
- 主机: Windows 11 @ 192.168.0.171
- 仓库路径: D:/DevProjects/ai-crm
- SSH 密钥已配置 (密码: 112233 per v2.4)
- VS Code + Claude Code 扩展

## 工作流程
1. PC3 提交 PR 后，OpenClaw 自动触发 PC4 审查
2. 审查结果: APPROVE → 流转 PC5 ｜ REJECT → 退回 PC3
3. 发现记录到 `brain/learnings/adversarial-findings.jsonl`

## 验收标准
- [ ] `/cso` 安全审查提示模板就绪
- [ ] 对 TASK-001 代码执行完整 OWASP Top 10 审查
- [ ] 输出结构化审查报告 (REJECT/APPROVE + 问题清单)
- [ ] 对抗性审查 prompt 模板验证有效

## 完成标记
完成后将本文件移至 tasks/done/ 并创建 TASK-003-done.md
