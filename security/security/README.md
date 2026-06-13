# PC4 安全审查基础设施 (v3.1.0)

PC4 是 AI-CRM 项目的首个自动化安全审查门禁，作为 SDLC (安全开发生命周期) 的第一道防线。
PC4 以对抗性思维审查每一次代码变更，覆盖 OWASP Top 10 (2021) 全部类别。

## 目录结构

```
security/
├── README.md                          # 本文件 — 安全审查基础设施总览
├── cso-review-prompt.md               # 对抗性安全审查提示词模板
├── review-report-template.md          # 审查报告输出模板
├── adversarial-review-checklist.md    # TASK-001 端点专项审查清单
├── run-security-review.sh             # Linux/macOS 审查启动脚本
├── run-adversarial-review.ps1         # Windows PowerShell 审查启动脚本
└── reports/                           # 审查报告存档目录
    └── .gitkeep                       # 保持目录在 git 中
```

## 快速开始

### 前置要求

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) 已安装并配置
- 项目仓库已克隆到本地
- Git 可用

### 运行一次安全审查

**Linux/macOS:**
```bash
# 审查指定 PR 编号
bash security/run-security-review.sh 42

# 审查指定分支
bash security/run-security-review.sh feature/TASK-001-crm-core-api
```

**Windows (PowerShell):**
```powershell
# 审查指定 PR 编号
.\security\run-adversarial-review.ps1 -PR "42"

# 审查指定分支
.\security\run-adversarial-review.ps1 -PR "feature/TASK-001-crm-core-api"
```

### 直接使用 Claude Code 进行审查

如果需要更灵活的控制，可以直接将提示词传给 Claude Code：

```bash
# 对整个仓库进行对抗性审查
claude -p "$(cat security/cso-review-prompt.md) — 审查当前仓库的完整代码"

# 对 TASK-001 模块进行端点级审查
claude -p "$(cat security/adversarial-review-checklist.md) — 按清单逐项审查"
```

### Claude Code `/cso` 斜杠命令

如果在 Claude Code 交互式会话中，可以使用内置斜杠命令：

```
/cso 审查 PR #42 — 对抗性安全审查, 覆盖 OWASP Top 10
```

`/cso` 命令会自动加载 `security/cso-review-prompt.md` 作为审查框架。

## 审查报告

所有审查报告保存在 `security/reports/` 目录下，命名格式:

```
pc4-review-pr{PR编号}-{ISO8601时间戳}.md
```

例如: `pc4-review-pr42-20260611T143052Z.md`

报告使用 `security/review-report-template.md` 中定义的模板格式。

### 报告判定级别

| 判定 | 含义 | 处理 |
|------|------|------|
| **APPROVED** | 无阻塞性问题 | 可以合并 |
| **CONDITIONAL APPROVAL** | 仅有非阻塞性问题 | 修复后合并，但可先合入 |
| **REJECTED** | 存在阻塞性问题 | 必须修复后重新审查 |

### 发现问题严重级别

| 级别 | 说明 | 示例 |
|------|------|------|
| **CRITICAL** | 可直接导致系统被完全入侵 | 未认证的 RCE、SQL 注入泄露全部数据 |
| **HIGH** | 可导致数据泄露或权限提升 | IDOR 泄露 PII、存储型 XSS |
| **MEDIUM** | 削弱安全态势 | CSRF、缺失安全头、信息泄露 |
| **LOW** | 最佳实践偏离 | 非敏感的 verbose 错误 |
| **INFO** | 纵深防御建议 | 可选的 CSP 细化 |

## 审查覆盖范围

### OWASP 2021 全面覆盖

| 类别 | 检查内容 |
|------|---------|
| A01 访问控制失效 | 认证中间件、IDOR、权限提升、JWT 验证、CORS |
| A02 加密失效 | TLS、密码哈希、密钥管理、弱加密算法 |
| A03 注入 | SQLi、NoSQLi、命令注入、模板注入、表达式注入 |
| A04 不安全设计 | 竞争条件、状态机绕过、业务逻辑缺陷 |
| A05 安全配置错误 | 安全头、错误暴露、调试端点、目录列表 |
| A06 易受攻击组件 | 依赖 CVE、EOL 库、依赖混淆 |
| A07 认证失效 | 密码策略、暴力破解防护、会话管理、MFA |
| A08 数据完整性失效 | 不安全反序列化、原型污染、CI/CD 完整性 |
| A09 日志监控失效 | 审计日志、敏感数据记录、告警、日志完整性 |
| A10 SSRF | 服务端请求、URL 白名单、内部 IP 阻止 |

### 专项检查

- [x] 硬编码密钥扫描
- [x] 输入验证完整性
- [x] 认证/授权检查覆盖
- [x] 不安全反序列化检测
- [x] 错误信息泄露检查
- [x] 文件上传安全检查
- [x] API 速率限制检查
- [x] 路径穿越检查
- [x] 命令注入检查

## OpenClaw 集成

PC4 可通过 OpenClaw 触发器在特定事件时自动运行审查:

### PR 触发审查
在 OpenClaw 配置中添加触发器，使得新的 PR 自动触发 PC4 审查:

```yaml
triggers:
  - event: pull_request.opened
    action: security-review
    prompt: "/cso 审查 PR #{{PR_NUMBER}}"
```

### 定时审查
```yaml
triggers:
  - schedule: "0 9 * * 1"  # 每周一早 9 点
    action: security-review
    prompt: "/cso 全量仓库对抗性安全审查"
```

## 常见问题

### Q: 审查脚本报错 "未找到 claude 命令"
A: 确保已安装 Claude Code CLI，并且 `claude` 命令在 PATH 中。
   安装指引: https://docs.anthropic.com/en/docs/claude-code/overview

### Q: 如何只审查特定模块？
A: 将模块代码路径直接传入提示词:
```bash
claude -p "$(cat security/cso-review-prompt.md) — 只审查 backend/app/api/customers.py"
```

### Q: 审查耗时多久？
A: 取决于变更大小。小型 PR (几十行) 约 1-3 分钟，大型 PR (几百行+) 约 3-10 分钟。

### Q: 发现记录存储在哪里？
A: `brain/learnings/adversarial-findings.jsonl` — JSONL 格式，每行一条发现记录。

### Q: 报告可以自动发布到 PR 吗？
A: 可以。在 CI/CD 流水线中添加步骤，将报告内容作为 PR Comment 发布。

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v3.1.0 | 2026-06-11 | PC4 安全审查基础设施初始版本。OWASP 2021 全覆盖、TASK-001 专项清单、Bash/PS 双平台脚本。 |

---

*PC4 安全审查基础设施 — "找到每一个漏洞。"*
