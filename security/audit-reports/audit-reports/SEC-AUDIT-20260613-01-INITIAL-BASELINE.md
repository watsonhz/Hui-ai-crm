# 安全审查报告 — 初始安全基线

---

## 审查元信息

| 字段 | 内容 |
|------|------|
| **报告编号** | SEC-AUDIT-20260613-01 |
| **审查日期** | 2026-06-13 |
| **审查人** | PC4 - Security Auditor |
| **审查分支** | feature/TASK-003-security-setup |
| **审查范围** | 后端 Python (FastAPI + SQLAlchemy) + 前端 (React + Vite) |
| **代码版本** | 4c8f383 |
| **审查结论** | ❌ 不通过 — 存在 P0 阻断性问题 |

---

## 审查摘要

| 严重程度 | 数量 | 状态 |
|----------|------|------|
| P0 阻断性 | 1 | 必须修复 |
| P1 严重 | 1 | 强烈建议修复 |
| P2 建议 | 2 | 可后续迭代修复 |

---

## 发现问题

### [P0-001] 默认 SECRET_KEY 为弱口令，生产环境可被伪造JWT

- **严重程度**: P0 阻断性
- **OWASP 分类**: A02:2021 – Cryptographic Failures
- **文件位置**: `backend/app/core/config.py:29`
- **CWE 编号**: CWE-798 (使用硬编码凭据)
- **问题描述**: 
  `SECRET_KEY` 默认值为 `"change-me-to-a-random-string"`，如果部署时未通过环境变量覆盖，攻击者可轻易伪造 JWT Token 获取任意用户权限。

- **攻击场景**: 
  1. 部署者忘记设置 `SECRET_KEY` 环境变量
  2. 攻击者得知该字符串为公开默认值
  3. 攻击者使用该密钥伪造 admin 权限的 JWT Token
  4. 攻击者获得系统最高权限

- **风险评估**: 
  - **影响范围**: 全局认证体系
  - **利用难度**: 低 (公开默认值)
  - **CVSS 评分**: 9.8 (Critical)

- **修复建议**: 
  移除默认值，强制启动时从环境变量读取，或使用 `secrets` 模块生成强随机密钥。

- **修复代码**:
```diff
-     SECRET_KEY: str = "change-me-to-a-random-string"
+     SECRET_KEY: str  # 移除默认值，强制从环境变量读取
```

或启动时添加运行时检查:
```python
# main.py 启动时
import secrets
if settings.SECRET_KEY == "change-me-to-a-random-string":
    import logging
    logging.critical("SECRET_KEY 未更改！请设置环境变量 SECRET_KEY")
    # 开发环境可自动生成
    if settings.APP_ENV == "development":
        settings.SECRET_KEY = secrets.token_urlsafe(64)
        logging.warning(f"开发环境已自动生成 SECRET_KEY")
    else:
        raise RuntimeError("生产环境必须设置 SECRET_KEY 环境变量")
```

---

### [P1-001] 数据库连接字符串硬编码凭据

- **严重程度**: P1 严重
- **OWASP 分类**: A02:2021 – Cryptographic Failures
- **文件位置**: `backend/app/core/config.py:19`
- **CWE 编号**: CWE-798
- **问题描述**: 
  `DATABASE_URL` 默认值 `"mysql+pymysql://crm_user:crm_pass@localhost:3306/ai_crm"` 包含明文用户名和密码。虽然可通过环境变量覆盖，但默认值中硬编码凭据违反安全最佳实践。

- **修复建议**: 
  默认值中移除凭据，或使用单独的 DB_USER/DB_PASS 环境变量拼接。

- **修复代码**:
```diff
-     DATABASE_URL: str = "mysql+pymysql://crm_user:crm_pass@localhost:3306/ai_crm"
+     DB_HOST: str = "localhost"
+     DB_PORT: int = 3306
+     DB_USER: str = ""
+     DB_PASS: str = ""
+     DB_NAME: str = "ai_crm"
+     
+     @property
+     def DATABASE_URL(self) -> str:
+         return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
```

---

### [P2-001] CORS 配置过于宽松

- **严重程度**: P2 建议
- **文件位置**: `backend/app/main.py:20-21`
- **问题描述**: 
  `allow_methods=["*"]` 和 `allow_headers=["*"]` 允许所有HTTP方法和请求头，增加攻击面。

- **修复建议**: 
  限制为实际需要的方法和头部。

- **修复代码**:
```diff
-     allow_methods=["*"],
-     allow_headers=["*"],
+     allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
+     allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
```

---

### [P2-002] 前端依赖存在已知漏洞

- **严重程度**: P2 建议
- **文件位置**: `frontend/package.json`
- **问题描述**: 
  npm audit 发现 2 个已知漏洞：
  - **esbuild <= 0.28.0** (间接依赖 via vite): HIGH — 缺少二进制完整性验证，可导致RCE (GHSA-gv7w-rqvm-qjhr)；MODERATE — 开发服务器允许任意网站读取响应 (GHSA-67mh-4wv8-2f99)
  - **vite <= 6.4.1** (直接依赖): MODERATE — 路径遍历漏洞 (GHSA-4w7w-66w2-5vf9)

- **修复建议**: 
  升级 vite 至 8.0.16+（需 major 升级），或至少升级至最新 5.x/6.x 补丁版本。esbuild 会随 vite 升级自动更新。

- **修复代码**:
```json
// package.json
"vite": "^5.4.0"  →  "vite": "^6.5.0"  // 或更高版本
```

---

## 安全基线检查

参照 `security/checklists/code-review-checklist.md`：

### SQL注入
- [x] 所有数据库查询使用参数化查询/ORM (SQLAlchemy ORM)
- [x] 无字符串拼接SQL
- [ ] 存储过程参数化 (暂无存储过程)

### XSS防护
- [ ] 所有用户输入输出进行HTML编码 (前端未审查)
- [x] API响应Content-Type正确设置 (application/json via FastAPI)
- [ ] CSP头配置 (未配置)

### 认证与授权
- [ ] JWT Token过期时间合理（8小时）(未实现JWT)
- [ ] 密码使用bcrypt/scrypt加密 (未实现认证)
- [ ] RBAC权限检查在每个端点 (未实现)
- [x] 无硬编码密钥/密码 → ❌ 发现 P0-001 & P1-001

### 数据安全
- [ ] 敏感字段加密存储（AES-256）(未实现)
- [ ] HTTPS强制（生产环境）(未部署)
- [x] 日志不含敏感信息（当前无日志代码）
- [ ] 文件上传限制类型和大小 (未实现)
- [ ] 操作日志保留90天可审计 (未实现)

### API安全
- [ ] 请求频率限制 (Rate Limiting) (未实现)
- [x] 输入参数校验（Pydantic已引入）
- [x] CORS白名单（仅允许内网IP）→ ❌ 方法/头部过宽 (P2-001)
- [ ] 错误信息不泄露内部细节 (无自定义异常处理)
- [x] API版本管理 (/api/v1/ 前缀)

### 政企合规
- [x] 数据本地存储（不离开局域网）(架构设计)
- [ ] 三重一大审批留痕 (未实现)
- [ ] 操作日志不可篡改 (未实现)
- [ ] 数据备份加密 (未实现)

---

## 自动化扫描结果

### Bandit (Python代码扫描)
- **扫描命令**: `bandit -r backend/`
- **扫描时间**: 2026-06-13
- **结果摘要**: 0 个问题 (bandit 未检测到默认值中的凭据问题，这些问题需要人工审查发现)

### pip-audit (Python依赖)
- **扫描命令**: `pip-audit -r backend/requirements.txt`
- **扫描时间**: 2026-06-13
- **结果摘要**: 无已知漏洞

### npm audit (前端依赖)
- **扫描命令**: `npm audit`
- **扫描时间**: 2026-06-13
- **结果摘要**: 2 个漏洞 (1 HIGH + 1 MODERATE)，详见 P2-002

---

## 审查结论

- [ ] ✅ 通过
- [x] ❌ 不通过 — 存在 1 个 P0 阻断性问题 (SECRET_KEY 硬编码默认值)，1 个 P1 严重问题 (数据库凭据硬编码)

### 修复后重审要求
1. P0-001: SECRET_KEY 移除默认值或添加强随机生成逻辑
2. P1-001: DATABASE_URL 拆分为独立环境变量
3. 建议一并修复 P2-001, P2-002

---

**签认**: PC4 安全审查工程师
**日期**: 2026-06-13
