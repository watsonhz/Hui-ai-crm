# PC4 对抗性审查清单 —— TASK-001 (CRM 核心 API)

> **目标**: 对 TASK-001 实现的 4 个模块、17+ 端点进行逐端点对抗性安全审查。
>
> **审查对象**:
> - 客户管理: `backend/app/api/customers.py` + `backend/app/services/customer_service.py` + `backend/app/schemas/customer.py` + `backend/app/models/customer.py`
> - 投标管理: `backend/app/api/bidding.py` + `backend/app/services/bidding_service.py` + `backend/app/schemas/bidding.py` + `backend/app/models/bidding.py`
> - 项目管理: `backend/app/api/projects.py` + `backend/app/services/project_service.py` + `backend/app/schemas/project.py` + `backend/app/models/project.py`
> - 组织层级: `backend/app/api/organizations.py` + `backend/app/services/organization_service.py` + `backend/app/schemas/organization.py` + `backend/app/models/organization.py`
> - 应用入口: `backend/app/main.py`
> - 配置: `backend/app/core/config.py`

---

## 一、全局级别检查 (Global)

### G-01: 认证与授权
- [ ] **[认证缺失]** 所有端点是否均无认证中间件？
  - 确认: `main.py` 中未注册任何认证依赖项，`customers.py` 等路由中无 `Depends(verify_token)` 等调用
  - 攻击面: 任何能访问服务的人可对全部 CRUD 端点和 `/docs`、`/redoc` 进行无限制操作
  - TASK-001 注释写明 "认证中间件后续添加"，当前状态是否为有意为之？
- [ ] **[授权缺失]** 所有端点均无 RBAC/ABAC 授权检查
  - 攻击者能否创建/修改/删除任意客户的任意数据？
  - `DELETE` 端点无任何权限控制，攻击者可批量软删除全量数据
- [ ] **[IDOR 风险]** `{customer_id}`, `{bidding_id}`, `{project_id}`, `{org_id}` 均为自增整数
  - 攻击者能否遍历 ID 枚举所有客户、投标、项目、组织数据？
  - 是否应该在返回数据中加入归属校验（如: 只返回当前用户拥有的数据）？

### G-02: 速率限制
- [ ] 所有端点均无速率限制
  - 攻击者能否通过高频调用 `/api/v1/customers/` 耗尽数据库连接池？
  - `/api/v1/customers/` POST 端点能否被用于批量创建海量垃圾数据？
  - 是否需要为所有端点添加 slowapi/rate-limit 中间件？

### G-03: 安全头配置
- [ ] `main.py` 仅注册了 CORS 中间件，缺少以下安全头:
  - [ ] `Content-Security-Policy`
  - [ ] `Strict-Transport-Security` (HSTS)
  - [ ] `X-Content-Type-Options: nosniff`
  - [ ] `X-Frame-Options: DENY`
  - [ ] `Referrer-Policy: strict-origin-when-cross-origin`
  - [ ] `Permissions-Policy`
- [ ] CORS 配置 `allow_methods=["*"]` + `allow_headers=["*"]` 是否过于宽松？

### G-04: 敏感信息暴露
- [ ] `docs_url="/docs"` + `redoc_url="/redoc"` — Swagger 文档在生产环境公开暴露
  - 攻击者可借此获取完整 API 清单、请求/响应 schema
  - 生产环境是否应禁用或要求认证才能访问？
- [ ] `config.py` 中硬编码默认数据库凭据:
  - [ ] `DATABASE_URL: str = "mysql+pymysql://crm_user:crm_pass@localhost:3306/ai_crm"` — 明文凭据
  - [ ] `SECRET_KEY: str = "change-me-to-a-random-string"` — 占位符是否被替换？
  - [ ] Redis URL `redis://localhost:6379/0` — 无密码
- [ ] 错误处理泄露异常消息: 如 `error(code=500, message=f"创建客户失败: {str(e)}")` 可能泄露内部状态

### G-05: 依赖项安全
- [ ] 检查 `requirements.txt` / `pyproject.toml` 中所有依赖是否存在已知 CVE
- [ ] FastAPI 版本、SQLAlchemy 版本、Pydantic 版本是否有已知安全漏洞？
- [ ] 是否使用了 `pickle`, `yaml.load`, `eval` 等危险函数？

---

## 二、客户管理 API (`/api/v1/customers`) 逐端点审查

### 2.1 POST /api/v1/customers — 创建客户

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无任何 Token 验证 |
| 输入验证-姓名 | 通过 | `min_length=1, max_length=100` |
| 输入验证-手机号 | 通过 | 正则 `^1[3-9]\d{9}$` |
| 输入验证-邮箱 | 通过 | 使用 Pydantic `EmailStr` |
| 输入验证-等级 | 通过 | 正则 `^[ABCD]$` |
| 输入验证-地址 | 待确认 | `max_length=500`，无 XSS 防护检查 |
| 输入验证-备注 | 待确认 | 无长度限制 (可导致 DoS 存储耗尽) |
| SQL 注入 | 通过 | 使用 SQLAlchemy ORM 参数化 |
| Mass Assignment | 待确认 | `Customer(**data.model_dump())` — 是否包含不期望的字段？ |
| XSS | 待确认 | 响应中 PII 字段无输出编码 |

**特殊攻击向量**:
- [ ] **[PII 泄露]** 创建后返回完整的 `CustomerResponse` 包含 `phone`, `email` — 任何人调用创建 API 即可看到返回的 PII
- [ ] **[备注字段 XSS]** `notes` 字段无 HTML 编码 — 如果前端直接渲染 HTML，则 `notes: "<script>alert(1)</script>"` 可导致存储型 XSS
- [ ] **[邮箱炸弹]** 无速率限制，攻击者可注册大量邮箱垃圾数据
- [ ] **[手机号枚举]** 通过创建同一手机号或邮箱，能否推断该客户是否已存在？

### 2.2 GET /api/v1/customers — 客户列表

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 任何人可读取全部客户数据 |
| 分页限制 | 部分通过 | `page_size` 最大 100，但 `page` 无上限 |
| 模糊搜索安全性 | 待确认 | `name.like(f"%{name}%")` — 是否存在 ReDoS？`%` 通配符本身是否被转义？ |
| 排序注入 | 通过 | sort_order 使用正则白名单 `^(name_asc\|name_desc\|created_asc\|created_desc)$` |
| SQL 注入 | 通过 | 使用 ORM 过滤 |
| PII 泄露 | 高风险 | 列表返回每个客户的 `phone`, `email` — 一次查询泄露所有客户的 PII |

**特殊攻击向量**:
- [ ] **[数据批量窃取]** 未认证的攻击者可通过分页遍历获取全部客户数据（含手机号和邮箱）
  - PoC: `curl http://192.168.0.170:8000/api/v1/customers?page=1&page_size=100`
- [ ] **[深度分页 DoS]** `page=9999999` 可导致数据库大 OFFSET 扫描
- [ ] **[ReDoS 风险]** `name=%25%25%25%25...(重复)` 在 SQL LIKE 中可能造成性能退化
- [ ] **[信息推断]** `status` 筛选使用正则 `^(active|inactive)$` — 但 schema 注释中有 `潜在/意向/谈判/成交/流失` 5 种状态，API 与 schema 不一致

### 2.3 GET /api/v1/customers/{customer_id} — 客户详情

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| 授权检查 | 缺失 | 无归属校验 — 任何 ID 都可以查看 |
| IDOR | 高风险 | `customer_id: int` 可枚举 |
| 404 信息泄露 | 通过 | 返回 "客户不存在"，不区分"不存在"与"无权限" |
| PII 泄露 | 高风险 | 响应包含完整 `phone`, `email`, `address` |

**特殊攻击向量**:
- [ ] **[批量 ID 枚举]** 攻击者可编写脚本从 ID=1 遍历到 ID=N，收集所有客户 PII
- [ ] **[竞态条件]** GET 操作无副作用，但若同时有 UPDATE 操作，是否存在 TOCTOU？

### 2.4 PUT /api/v1/customers/{customer_id} — 更新客户

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| 授权检查 | 缺失 | 任何人可修改任何客户 |
| IDOR | 高风险 | 可枚举 |
| Mass Assignment | 待确认 | `setattr(customer, key, value)` — 是否可以将 `id` 或其他敏感字段注入？ |
| 输入验证 | 通过 (同创建) | Phone/email 模式一致 |
| Status 转换 | 待确认 | status 只允许 `active/inactive`，但数据库设计中有 5 种状态枚举，是否有绕过？ |

**特殊攻击向量**:
- [ ] **[Mass Assignment to id]** `CustomerUpdate` 无 `id` 字段，但 Pydantic `exclude_unset` 只排除未设置的字段 — 若攻击者在请求体中发送 `{"id": 99999, "name": "hacked"}`，`id` 不在 schema 中会被忽略，确认安全
- [ ] **[Status 降级攻击]** 能否将活跃客户状态改为 inactive 从而"软驱逐"有效客户？
- [ ] **[数据完整性攻击]** 能否写空名称、非法手机号绕过 schema 校验？
  - Phone 正则在 `CustomerUpdate` 中存在，但值是 Optional — 设为 `null` 可清空手机号

### 2.5 DELETE /api/v1/customers/{customer_id} — 软删除客户

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| 授权检查 | 缺失 | 任何人可删除任何客户 |
| 防误删 | 无 | 无二次确认、无审计日志 |
| 恢复机制 | 无 | 软删除后无 API 恢复端点 |

**特殊攻击向量**:
- [ ] **[批量软删除]** 攻击者遍历 ID 1-N 可软删除全量客户数据
- [ ] **[删除 DoS]** 高频 DELETE 请求能否压垮数据库？

---

## 三、投标管理 API (`/api/v1/bidding`) 逐端点审查

### 3.1 POST /api/v1/bidding — 创建投标项目

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| 输入验证-金额 | 通过 | `gt=0, decimal_places=2` |
| 输入验证-概率 | 通过 | `ge=0, le=100` |
| 输入验证-状态 | 通过 | `field_validator` 检查 `BIDDING_STATUSES` |
| 输入验证-竞对信息 | 待确认 | `competitor_info` 无长度限制 (Text 类型) |
| 输入验证-备注 | 待确认 | `notes` 无长度限制 |
| SQL 注入 | 通过 | ORM 操作 |

**特殊攻击向量**:
- [ ] **[金额操纵-精度攻击]** `amount: Decimal(15, 2)` — 发送极大值如 `999999999999999.99` 是否被接受？
- [ ] **[状态跳过]** 创建时 `status` 默认"线索"，但可指定任意有效状态 — 能否创建时直接设为"中标"跳过全流程？
- [ ] **[竞对信息注入]** `competitor_info` 接受 Text 类型无限制 — 能否写入 XSS payload？能否写入数 GB 数据耗尽存储？
- [ ] **[日期操纵]** `bid_deadline` — 能否设为过去的日期？能否设为极远未来日期（如 9999-12-31）？

### 3.2 GET /api/v1/bidding — 投标列表

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| status 过滤注入 | 通过 | ORM == 等值匹配 |
| customer_name 模糊搜索 | 待确认 | `like(f"%{customer_name}%")` — LIKE 注入风险？ |
| 分页 | 通过 | 1-100 |

**特殊攻击向量**:
- [ ] **[敏感信息暴露]** 投标列表返回 `amount`, `competitor_info` — 竞争对手能否通过此接口获取我方的投标价格和策略？
- [ ] **[金额枚举]** 商业机密 `amount` 对所有人可见

### 3.3 GET /api/v1/bidding/calendar — 投标日历

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| days 参数 | 通过 | `ge=1, le=365` |

**特殊攻击向量**:
- [ ] **[信息聚合]** 日历视图汇总了未来所有投标截止日 — 攻击者可据此推断公司业务节奏和投标密集期
- [ ] **[数据泄露]** 日历项返回 `project_name`, `customer_name`, `bid_deadline` — 可构建完整投标情报

### 3.4 GET /api/v1/bidding/{bidding_id} — 投标详情

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| IDOR | 高风险 | bidding_id 可枚举 |
| 敏感数据 | 高风险 | 返回 `amount`, `competitor_info`, `probability`, `notes` |

### 3.5 PUT /api/v1/bidding/{bidding_id} — 更新投标/状态转换

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| 状态机校验 | 通过 | `ALLOWED_TRANSITIONS` 字典硬编码 |
| 终态保护 | 通过 | "丢标"/"维保" 无允许迁移 |
| Mass Assignment | 待确认 | 更新数据中分离 new_status 处理 |

**特殊攻击向量**:
- [ ] **[金额篡改]** 能否在"投标中"阶段修改 amount 为 0 或极大值？
- [ ] **[概率篡改]** 能否修改 `probability` 为 100% 伪造中标信心？
- [ ] **[日期篡改]** 能否修改已过期的 `bid_deadline`？
- [ ] **[状态跳跃-服务层]** API 层分离 `new_status` 和 `update_data`，但服务层 `update_bidding` 使用 `setattr` — 若攻击者在 `update_data` 中也包含 `status` 字段会怎样？`exclude_unset=True` 后 `model_dump` 不应包含 `status` 因为 `BiddingUpdate` 无 `status` 字段…确认安全
- [ ] **[并发状态竞争]** 两个请求同时更新同一投标的状态 — 是否有乐观锁保护？

### 3.6 DELETE /api/v1/bidding/{bidding_id} — 软删除投标

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |

**同客户模块的 DELETE 风险。**

---

## 四、项目管理 API (`/api/v1/projects`) 逐端点审查

### 4.1 POST /api/v1/projects — 创建项目

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 输入验证-金额 | 待确认 | 检查 `ProjectCreate` schema 是否包含 `amount` 的 `gt=0` 约束 |
| 输入验证-进度 | 待确认 | 检查 `progress` 范围 0-100 |
| 输入验证-日期 | 待确认 | `start_date` < `expected_end_date` 是否校验？ |
| Stage 默认值 | 通过 | 默认"初步接洽" |

**特殊攻击向量**:
- [ ] **[日期逻辑绕过]** `start_date` 晚于 `expected_end_date` 是否被接受？能否导致数据不一致？
- [ ] **[进度伪造]** 创建时直接设置 `progress=100` 是否被允许？

### 4.2 GET /api/v1/projects — 项目列表

**与投标列表类似的风险。**

### 4.3 GET /api/v1/projects/kanban — 看板视图

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |

**特殊攻击向量**:
- [ ] **[全量数据暴露]** 看板无分页，返回全部未删除项目 — 攻击者一次请求获取所有项目信息
- [ ] **[内存 DoS]** 若项目数量极大，看板视图可能消耗大量内存

### 4.4 PUT /api/v1/projects/{project_id}/stage — 推进阶段

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 阶段前向控制 | 通过 | `target_idx <= current_idx` → 拒绝 |
| 阶段有效性 | 通过 | `STAGE_INDEX` 映射检查 |

**特殊攻击向量**:
- [ ] **[阶段跳过]** 能否跳过中间阶段？例如从"初步接洽"直接到"商务谈判"？
  - 检查: `target_idx <= current_idx` 只阻止回退，不阻止跳跃
  - 攻击路径: 从"初步接洽"(idx=0) 直接发 `{"new_stage": "合同签订"}` (idx=5) — `5 > 0` 所以通过
  - 风险: 业务逻辑允许跳过关键中间阶段（需求分析、方案演示、报价、商务谈判）
  - **这是一个业务逻辑漏洞！**
- [ ] **[并发阶段竞争]** 两个请求同时推进阶段 — 可能导致阶段不一致

### 4.5 DELETE /api/v1/projects/{project_id} — 软删除项目

**同前述 DELETE 风险。**

### 4.6 PUT /api/v1/projects/{project_id} — 更新项目

**同投标更新风险。**

---

## 五、组织层级 API (`/api/v1/organizations`) 逐端点审查

### 5.1 POST /api/v1/organizations — 创建组织节点

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 输入验证-名称 | 待确认 | 检查 `OrgCreate` schema 约束 |
| 层级校验 | 通过 | 服务层验证 `data.level == parent.level + 1` |
| 父节点存在性 | 通过 | 查询确认 |

**特殊攻击向量**:
- [ ] **[层级越权]** 能否直接创建 level=1（大区）节点从而成为顶级管理员可见的组织？
- [ ] **[循环引用]** parent_id 能否指向自身或子节点形成循环？服务层仅检查父节点存在性，未检查循环
  - 攻击路径: 创建 A(level=1) -> 创建 B(level=2, parent=A) -> 更新 A 的 parent_id 为 B
  - 后果: 递归查询 `_build_org_node` 进入无限循环，导致栈溢出 (StackOverflow)
  - **这是一个潜在的拒绝服务漏洞！**
- [ ] **[sort_order 溢出]** sort_order 为 int 类型，可设为极大值或负值

### 5.2 GET /api/v1/organizations/tree — 组织树

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 暴露完整组织架构 |

**特殊攻击向量**:
- [ ] **[组织情报泄露]** 组织树暴露公司完整管理层级结构，可用于社会工程学攻击
- [ ] **[N+1 查询放大]** `_build_org_node` 递归遍历 children relationship — 大组织树可能导致数据库查询风暴

### 5.3 DELETE /api/v1/organizations/{org_id} — 删除组织 (硬删除!)

| 检查项 | 状态 | 说明 |
|-------|------|------|
| 认证检查 | 缺失 | 无 |
| 子节点保护 | 通过 | 有子节点时拒绝删除 |
| **硬删除 vs 软删除** | **高风险** | `db.delete(instance)` 是物理删除，而其他模块均为软删除 — 不一致 |
| 无审计日志 | 缺失 | 硬删除无任何记录，不可恢复 |

**特殊攻击向量**:
- [ ] **[拒绝服务]** 删除叶子节点后，该节点的历史数据关联可能断开（如果有 FK 约束）
- [ ] **[物理删除不可恢复]** 误操作或恶意操作导致数据永久丢失

---

## 六、业务逻辑特定审查

### 6.1 投标状态机 (9 态)
- [ ] 状态转换是否在服务端验证？（是）
- [ ] 终态是否真正不可转换？（是，"丢标"/"维保" 的 allowed 集合为空）
- [ ] 是否存在并发绕过：两个请求同时转换同一投标的状态？
- [ ] 能否通过直接修改数据库绕过状态机？
- [ ] **[金额篡改]** 在"投标中"阶段能否修改金额？应该锁定

### 6.2 项目阶段流转 (12 阶段)
- [ ] **阶段跳跃漏洞确认**: 仅校验"不回退"，未校验"必须按序"
  - 必须修复: 添加 `target_idx == current_idx + 1` 的严格校验
  - 或定义 `ALLOWED_NEXT_STAGE` 映射类似 bidding 的 `ALLOWED_TRANSITIONS`
- [ ] 能否并发推进导致阶段跳过？

### 6.3 客户归属
- [ ] 当前无客户归属概念 (`owner_id` 存在于数据库中但未在 API 中使用)
- [ ] 任何用户可操作任何客户的数据 — 完全的 IDOR

### 6.4 数据暴露
- [ ] 列表 API 返回完整实体而非摘要 — 手机号、邮箱、金额全部暴露
- [ ] 无字段级别权限控制 — 应该实现"列表返回摘要，详情返回完整"或字段掩码

---

## 七、配置安全检查

### 7.1 config.py 硬编码凭据
- [ ] `DATABASE_URL` — 包含明文密码 `crm_pass`
- [ ] `SECRET_KEY` — 占位符值 `change-me-to-a-random-string`
- [ ] `REDIS_URL` — 无密码
- [ ] 这些值应通过环境变量注入，不应有默认值

### 7.2 main.py 安全配置
- [ ] `/docs`, `/redoc` 在生产环境应禁用或要求认证
- [ ] 应添加 TrustedHostMiddleware 防止 Host Header 攻击
- [ ] 应添加 GZipMiddleware 的压缩炸弹保护

### 7.3 .env 文件
- [ ] 检查 `.env` 是否被加入 `.gitignore`
- [ ] 检查 `.env.example` 是否包含真实凭据

---

## 八、SQL 注入专项审查

### 8.1 LIKE 查询注入
所有模糊搜索使用:
```python
query.filter(Model.field.like(f"%{user_input}%"))
```
- `%` 和 `_` 是 LIKE 通配符 — 攻击者输入 `%` 会匹配所有记录
- 但不会导致 SQL 注入，因为 SQLAlchemy 参数化处理
- 风险等级: LOW (可能导致非预期的全量匹配而非注入)

### 8.2 排序字段
`customers` 路由中的 `sort_order` 使用正则白名单，安全。
其他模块无用户可控排序字段，使用硬编码 `updated_at.desc()`。

### 8.3 整体评估
SQL 注入风险: **低** — 全部使用 SQLAlchemy ORM，无字符串拼接 SQL。
但 `(("" 导出))` 等需要审查任何原生 SQL 查询。

---

## 九、XSS 检查

- [ ] `notes`, `competitor_info`, `address` 等 Text 字段无 HTML 净化
- [ ] 如果前端直接使用 `innerHTML` 渲染或 React 的 `dangerouslySetInnerHTML`，则存在存储型 XSS
- [ ] API 响应本身为 JSON，浏览器不执行 JSON — 风险在前端渲染层
- [ ] 建议: API 应对自由文本字段进行 HTML 编码 或 前端使用安全的文本渲染方式

---

## 十、审查结论模板

每个检查项标记为:
- **PASS**: 安全检查通过
- **FAIL**: 存在安全漏洞，必须修复
- **NA**: 不适用
- **WARN**: 需要关注但非阻塞

汇总:
| 类别 | PASS | FAIL | WARN | NA |
|------|------|------|------|-----|
| 认证/授权 | 0 | 17+ | 0 | 0 |
| 输入验证 | | | | |
| SQL 注入 | | | | |
| XSS | | | | |
| 业务逻辑 | | | | |
| 配置安全 | | | | |
| PII 保护 | | | | |

---

*PC4 对抗性审查清单 v3.1.0 — 基于 TASK-001 实际代码审计生成*
