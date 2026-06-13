# /cso-sprint3 — Sprint3 安全审查一键工作流

## 触发时机
PC3/PC2 提交 TASK-009/TASK-010 代码后立即执行。

## 一键执行

```bash
cd C:\DevProjects\ai-crm

# ── Stage 1: 自动化扫描 ──
echo "=== Bandit AI/服务扫描 ==="
cd backend
bandit -r app/services/report_generator.py app/services/vector_service.py app/api/v1/ai/ app/api/v1/knowledge.py -f txt -o ../security/scan-results/sprint3-bandit.txt 2>&1
bandit -r app/services/ app/api/v1/ai/ app/api/v1/knowledge.py -f html -o ../security/scan-results/sprint3-bandit.html 2>&1

echo "=== pip-audit 依赖检查 ==="
cd ..
pip-audit -r backend/requirements.txt 2>&1 | tee security/scan-results/sprint3-pipaudit.txt

echo "=== npm audit 前端检查 ==="
cd frontend
npm audit 2>&1 | tee ../security/scan-results/sprint3-npm-audit.txt

# ── Stage 2: 手工审查 (Claude Code) ──
# 打开每个目标文件，逐项对照检查清单

# ── Stage 3: 报告输出 ──
# 使用 security/audit-reports/AUDIT-REPORT-TEMPLATE.md
# 输出: security/audit-reports/SEC-AUDIT-20260615-SPRINT3-FINAL.md
```

## 手工审查执行清单

对每个新文件执行以下 grep + 人工读取：

### AI 报告生成
```bash
grep -n "prompt\|system_message\|instruction\|raw_" backend/app/services/report_generator.py
grep -n "model\.\|completion\|chat\.\|anthropic\|openai\|deepseek\|llm" backend/app/services/report_generator.py
grep -n "input\|user_input\|request\|form" backend/app/api/v1/ai/reports.py
```

### 向量检索
```bash
grep -n "embed\|vector\|similarity\|top_k\|metadata\|namespace\|collection" backend/app/services/vector_service.py
grep -n "filter\|tenant\|user_id\|org_id" backend/app/services/vector_service.py backend/app/api/v1/knowledge.py
```

### 合同 (支付安全)
```bash
grep -rn "amount\|金额\|price\|money\|Decimal\|float" frontend/src/views/contracts/
grep -rn "dangerouslySetInnerHTML\|v-html\|innerHTML\|dangerouslyUseHTMLString" frontend/src/views/contracts/
```

### 文件上传
```bash
grep -rn "upload\|multipart\|File\|file\|mime\|extension" backend/app/api/v1/knowledge.py
```

## 审查维度速查

| # | 维度 | 检查关键词 |
|---|------|-----------|
| 1 | Prompt Injection | 用户输入→prompt 拼接, 无分隔符 |
| 2 | AI 输出 XSS | LLM输出→HTML渲染, 无转义 |
| 3 | 多租户泄露 | 向量检索无 tenant filter |
| 4 | 金额篡改 | 前端金额可改, Decimal vs float |
| 5 | 文件上传 | 无类型限制, 无大小限制, 路径穿越 |
| 6 | 认证缺失 | 新端点无 Depends(get_current_user) |
| 7 | SSRF | LLM/tool 调用可指定 URL |
