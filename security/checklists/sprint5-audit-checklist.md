# Sprint5 安全审查清单 — AI销售+营销+RBAC权限+图谱XSS+操作日志

## 1. AI 销售引擎

### 线索评分逻辑安全
- [ ] 评分公式是否可被用户输入操纵
- [ ] 模型输入特征是否经过校验
- [ ] 评分结果是否影响自动化决策（GDPR 合规）
- [ ] 评分模型是否有对抗样本防护

### 流失预测
- [ ] 预测输入是否包含敏感字段
- [ ] 预测结果是否会泄露其他客户数据
- [ ] 批量预测是否有速率限制

**审计命令**:
```bash
grep -rn "scoring\|lead_score\|churn\|predict\|classifier" backend/app/services/
grep -rn "feature\|weight\|coefficient\|threshold" backend/app/services/
```

---

## 2. AI 营销内容生成

### 内容注入
- [ ] 用户输入的营销参数是否直接拼入 prompt
- [ ] 生成内容是否经过安全过滤再发布
- [ ] 是否有内容审核机制（敏感词/竞品提及）
- [ ] 生成内容中的链接是否校验（防钓鱼）

### 模板安全
- [ ] 营销模板是否可被注入（Jinja2/SSTI）
- [ ] 模板变量是否做 HTML 转义
- [ ] 模板来源是否有白名单

**审计命令**:
```bash
grep -rn "marketing\|content_gen\|template\|jinja" backend/ --include="*.py"
grep -rn "autoescape\|mark_safe\|safe" backend/ --include="*.py"
```

---

## 3. RBAC 权限系统

### 权限模型
- [ ] 角色定义是否不可被前端篡改
- [ ] 权限检查是在后端逐接口执行
- [ ] 角色变更是否需 admin 权限
- [ ] 是否有默认拒绝策略（deny-by-default）

### 越权测试
- [ ] 普通用户能否访问 admin 接口
- [ ] 用户能否通过修改请求参数查看他人数据
- [ ] 角色删除/降级是否有保护措施

### 操作日志
- [ ] 权限变更是否记录审计日志
- [ ] 日志是否包含 who/when/what/IP
- [ ] 日志是否可被管理员删除/篡改
- [ ] 日志存储是否有保留期限

**审计命令**:
```bash
grep -rn "role\|permission\|rbac\|check_permission\|require_role" backend/ --include="*.py"
grep -rn "audit\|log\|audit_log\|operation_log\|action_log" backend/ --include="*.py"
```

---

## 4. 知识图谱 XSS

### 节点数据注入
- [ ] 节点 label/tooltip 是否渲染为 HTML
- [ ] 节点属性中的用户数据是否转义
- [ ] 图谱库 (ECharts Graph / D3 / vis.js) 配置是否有 XSS 向量
- [ ] 图谱搜索查询是否可注入

**审计命令**:
```bash
grep -rn "graph\|graphviz\|relation\|节点\|图谱\|echarts.*graph\|d3\|vis" frontend/src/ --include="*.vue" --include="*.ts"
grep -rn "dangerouslySetInnerHTML\|v-html\|innerHTML" frontend/src/views/graph/
```

---

## 5. 操作日志完整性

### 防篡改
- [ ] 日志是否写入后不可修改 (append-only)
- [ ] 是否有日志完整性校验 (hash chain/Merkle)
- [ ] 日志存储是否独立于业务库

### 日志内容
- [ ] 是否记录: 操作人/时间/IP/操作类型/目标对象/变更前后
- [ ] 不记录敏感字段明文 (密码/Token)
- [ ] 日志保留期是否 ≥ 90 天 (政企合规)

**审计命令**:
```bash
grep -rn "audit_log\|operation_log\|create_log\|log_action" backend/ --include="*.py"
grep -rn "hash\|checksum\|tamper\|immutable\|append_only" backend/ --include="*.py"
```

---

## Sprint5 风险矩阵

| 风险 | 概率 | 影响 | 优先级 |
|------|:--:|:--:|:--:|
| SSTI via Jinja2 模板 | 中 | 极高 | **P0** |
| RBAC 越权提权 | 高 | 极高 | **P0** |
| AI 内容无审核发布 | 高 | 高 | **P0** |
| 营销内容 XSS | 高 | 高 | **P1** |
| 图谱节点 XSS | 中 | 高 | **P1** |
| 操作日志可篡改 | 低 | 极高 | **P1** |
| 评分模型对抗 | 低 | 中 | **P2** |

## Sprint5 审计命令一览
```bash
# 代码注入
bandit -r backend/app/services/ai_sales/ backend/app/services/ai_marketing/
grep -rn "Template\|jinja2\|mark_safe\|autoescape" backend/

# RBAC
grep -rn "role\|permission\|check_perm\|require_admin" backend/app/core/
grep -rn "role\|permission" backend/app/api/v1/admin/

# 日志
grep -rn "audit\|log\|操作日志" backend/app/services/ backend/app/api/

# 图谱
grep -rn "v-html\|dangerouslySetInnerHTML\|innerHTML" frontend/src/views/graph/
```
