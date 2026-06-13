---
task_id: TASK-003
title: PC4安全审计环境搭建 + 初始安全扫描
assignee: pc4
role: security-auditor
priority: P0 (最高)
deadline: 2026-06-14
branch: feature/TASK-003-security-setup
dependencies: []
tags: [security, audit, cso, sprint1]
---

# TASK-003：PC4安全审计环境搭建 + 初始安全扫描

## 需求描述
搭建安全审计工具链，对现有代码库进行首次全量安全扫描，建立安全基线。

## 具体任务

### 1. 安装安全审计工具
```bash
pip install bandit==1.7.0        # Python代码安全扫描
pip install safety==2.3.0        # 依赖漏洞检查
npm install -g eslint-plugin-security  # JS安全规则
```

### 2. 对现有代码运行首次扫描
```bash
cd C:\DevProjects\ai-crm\backend
bandit -r . -f html -o ..\security\scan-results\bandit-initial.html
bandit -r . -f txt -o ..\security\scan-results\bandit-initial.txt

cd C:\DevProjects\ai-crm\frontend
npm audit --json > ..\security\scan-results\npm-audit-initial.json
```

### 3. 创建安全审查报告模板
在 security/audit-reports/ 下创建报告模板，参照 security/checklists/code-review-checklist.md

### 4. 准备 /cso 工作流
标准化安全审查流程：bandit → safety → Claude Code深度分析 → 签认报告

## 验收标准
- [ ] bandit 安装并运行成功
- [ ] safety 安装并运行成功
- [ ] 初始扫描报告生成
- [ ] 安全审查报告模板就位
- [ ] /cso 工作流可执行

## 完成标记
完成后将本文件移至 tasks/done/
