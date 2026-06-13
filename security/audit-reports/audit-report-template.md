# 安全审计报告

**审计日期:** {{date}}
**审计人员:** PC4 (Security Auditor)
**PR/分支:** {{pr_or_branch}}
**审查范围:** {{scope}}

---

## 一、执行摘要

| 项目 | 结果 |
|------|------|
| 审计结论 | ☐ APPROVE / ☐ REJECT |
| 高危问题 | {{high_count}} |
| 中危问题 | {{medium_count}} |
| 低危问题 | {{low_count}} |
| 审计耗时 | {{duration}} |

## 二、扫描结果

### 2.1 Bandit 静态分析
- 扫描文件: {{bandit_files_scanned}}
- 发现问题: {{bandit_issues}}
- 报告: `security/scan-results/bandit-initial.html`

### 2.2 依赖漏洞检查
- 扫描依赖: {{deps_count}}
- 已知漏洞: {{vuln_count}}
- 报告: `security/scan-results/safety-initial.json`

## 三、OWASP Top 10 审查明细

### SQL 注入
- [ ] 参数化查询: {{sql_result}}
- 发现问题: {{sql_issues}}

### XSS 防护
- [ ] HTML 编码: {{xss_result}}
- 发现问题: {{xss_issues}}

### 认证与授权
- [ ] JWT / RBAC: {{auth_result}}
- 发现问题: {{auth_issues}}

### 敏感数据泄露
- [ ] 加密存储 / 无硬编码密钥: {{data_result}}
- 发现问题: {{data_issues}}

### API 安全
- [ ] Rate Limit / CORS / 输入校验: {{api_result}}
- 发现问题: {{api_issues}}

## 四、问题清单

| # | 严重度 | 类别 | 文件:行号 | 描述 | 修复建议 |
|---|--------|------|-----------|------|----------|
| 1 | | | | | |
| 2 | | | | | |

## 五、合规检查

| 要求 | 状态 | 备注 |
|------|------|------|
| 数据本地存储 | ☐ 通过 / ☐ 未通过 | |
| 三重一大留痕 | ☐ 通过 / ☐ 未通过 | |
| 日志不可篡改 | ☐ 通过 / ☐ 未通过 | |
| 备份加密 | ☐ 通过 / ☐ 未通过 | |

## 六、签认

- **审计人 (PC4):** ___________ 日期: ___________
- **复审人 (PC1):** ___________ 日期: ___________
