# Sprint3 安全审查清单 — AI + 知识库 + 合同验收

## 1. AI 报告生成 (report_generator.py / reports.py)

### Prompt Injection (提示注入)
- [ ] 用户输入是否直接拼接到 LLM prompt 中（无清理/无分隔符）
- [ ] 是否有 prompt 越狱防护（"忽略上述指令"类攻击）
- [ ] LLM 输出长度是否限制（防止无限 token 消耗/DoS）
- [ ] LLM 输出是否渲染为 HTML（XSS via AI output）
- [ ] AI 生成内容是否标记为 "AI生成"（防止冒充人工）

### 数据泄露
- [ ] 报告生成时是否暴露了其他用户的数据（上下文混淆）
- [ ] 向量检索结果是否包含其他租户的文档块
- [ ] LLM API 调用的 prompt 中是否包含敏感字段（密码/手机号/身份证）

### API 安全
- [ ] 报告 API 是否有认证 (JWT Bearer)
- [ ] 报告 API 是否有速率限制（防止 LLM 资源耗尽攻击）
- [ ] 报告生成是否超时控制（防止长时间阻塞）

**审计命令**:
```bash
bandit -r backend/app/services/report_generator.py backend/app/api/v1/ai/
grep -rn "prompt\|instruction\|system_message" backend/app/services/
grep -rn "openai\|anthropic\|llm\|model.invoke\|completion" backend/app/services/
```

---

## 2. RAG 向量检索 (vector_service.py / knowledge.py)

### 数据隔离
- [ ] 向量检索是否带租户/用户过滤（多租户隔离）
- [ ] 是否有 collection/namespace 级别的访问控制
- [ ] top-K 结果是否做过敏感信息过滤

### 注入风险
- [ ] 用户查询是否直接作为向量检索输入（无清洗）
- [ ] 检索到的文本块是否在注入 LLM 前经过清理
- [ ] 向量数据库连接是否有认证（API Key / Token）

### 知识库 API
- [ ] 知识库 CRUD 是否有认证
- [ ] 文件上传是否有类型/大小限制
- [ ] 知识库文档的访问权限是否校验

**审计命令**:
```bash
grep -rn "chromadb\|pgvector\|pinecone\|milvus\|weaviate\|qdrant" backend/
grep -rn "embedding\|vector\|similarity_search\|top_k\|retrieve" backend/
grep -rn "upload\|file\|document\|multipart" backend/app/api/v1/knowledge.py
```

---

## 3. 合同页面 (contracts/)

### 支付安全
- [ ] 合同金额是否在客户端可篡改（前端计算 vs 后端计算）
- [ ] 合同金额提交是否在后端做二次校验
- [ ] 支付金额字段精度是否使用 Decimal（不是 float）
- [ ] 金额传输是否使用 HTTPS

### 签名/认证
- [ ] 合同签字是否有二次确认（防止 CSRF 一键签）
- [ ] 签名操作是否校验用户身份
- [ ] 合同状态流转是否有权限控制

**审计命令**:
```bash
grep -rn "amount\|金额\|price\|价格\|money\|合同额" frontend/src/views/contracts/
grep -rn "dangerouslySetInnerHTML\|v-html\|innerHTML" frontend/src/views/contracts/
```

---

## 4. 验收页面 (acceptance/) ✅ 已完成

- [x] P0-001: dangerouslyUseHTMLString XSS — 已修复 (escapeHtml)
- [x] P2-001: ::v-deep → :deep() — 已修复
- [ ] 验收驳回理由是否有长度限制（防止存储耗尽）
- [ ] 验收标准是否在后端做业务规则校验

---

## 5. 公共检查 (适用所有新代码)

### 认证授权
- [ ] 所有新端点是否有 `Depends(get_current_user)`
- [ ] 跨用户数据访问是否有所有权校验
- [ ] admin 权限操作是否有审计日志

### 依赖安全
```bash
pip-audit -r backend/requirements.txt
npm audit --prefix frontend/
```

### 代码扫描
```bash
bandit -r backend/app/services/ backend/app/api/v1/ai/ backend/app/api/v1/knowledge.py
```

---

## Sprint3 风险评估矩阵

| 风险 | 领域 | 概率 | 影响 | 优先级 |
|------|------|:--:|:--:|:--:|
| Prompt Injection | AI | 高 | 高 | **P0** |
| AI 输出 XSS | AI | 高 | 高 | **P0** |
| 金额篡改 | 合同 | 中 | 极高 | **P0** |
| 多租户数据泄露 | RAG | 中 | 极高 | **P1** |
| 文件上传攻击 | 知识库 | 中 | 高 | **P1** |
| LLM DoS | AI | 高 | 中 | **P2** |
| 向量注入 | RAG | 低 | 高 | **P2** |
