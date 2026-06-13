# /cso (Code Security Overview) — 安全审查 SOP

## 用途
PC4 安全审查工程师的标准操作流程。每次 PC3 提交 PR 后执行。

## 触发命令
```
/cso PR-XXX
```

## 执行流程

### Stage 1: 自动化工具扫描
```bash
# 1.1 Python代码安全扫描 (bandit)
cd C:\DevProjects\ai-crm\backend
bandit -r . -f html -o ..\security\scan-results\bandit-PR-XXX.html
bandit -r . -f txt -o ..\security\scan-results\bandit-PR-XXX.txt

# 1.2 Python依赖漏洞检查 (pip-audit)
cd C:\DevProjects\ai-crm
pip-audit -r backend/requirements.txt

# 1.3 前端依赖安全检查 (npm audit)
cd C:\DevProjects\ai-crm\frontend
npm audit
```

### Stage 2: Claude Code 深度分析
读取变更文件后，按以下维度逐文件审查：

1. **SQL注入** — 是否使用参数化查询/ORM，无字符串拼接
2. **XSS** — 用户输入是否转义，Content-Type是否正确
3. **认证授权** — JWT验证/权限检查是否完整
4. **敏感数据** — 密码/Token/密钥是否加密存储，无硬编码
5. **API安全** — CORS配置/速率限制/输入校验
6. **日志安全** — 是否泄露敏感信息
7. **支付安全** — (Pay场景) 金额篡改/签名绕过/回调伪造/并发

### Stage 3: 签认报告
使用 `security/audit-reports/AUDIT-REPORT-TEMPLATE.md` 模板，
生成 `security/audit-reports/SEC-AUDIT-YYYYMMDD-PR-XXX.md`

## 审查标准

### P0 阻断性 — 必须修复，否则不可上线
- 硬编码密钥/密码/Token
- SQL注入漏洞
- 认证绕过
- 支付金额可篡改
- 敏感数据明文泄露

### P1 严重 — 强烈建议修复
- XSS漏洞
- CSRF未防护
- 越权风险
- 日志泄露敏感信息
- 不安全的加密算法 (MD5/SHA1)

### P2 建议 — 可后续迭代修复
- CORS配置过宽
- 缺少速率限制
- 输入校验不足（非安全关键）
- 代码规范与最佳实践

## 输出要求
- 每个问题附带：文件位置、问题描述、攻击场景、修复建议、修复代码
- 审查结论：通过/不通过
- 不通过时明确打回 PC3 的修复要求

## 相关文件
- 审查清单: `security/checklists/code-review-checklist.md`
- 报告模板: `security/audit-reports/AUDIT-REPORT-TEMPLATE.md`
- 扫描结果: `security/scan-results/`
- 安全Prompt: `docs/prompts/security-audit-prompt.md`
