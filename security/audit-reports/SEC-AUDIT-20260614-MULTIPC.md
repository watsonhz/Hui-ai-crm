# 多PC合并安全审查 — 新模块认证审计

**日期**: 2026-06-14 | **审查人**: PC4

---

## P0 阻断: 10个新API模块无认证

以下模块由 PC2/PC3 合入，**所有端点均缺少 `Depends(get_current_user)`**：

| 模块 | 端点 | 风险 |
|------|:--:|------|
| acceptance | 3 | 验收数据裸奔 |
| ai_diagnosis | 1 | 诊断报告泄露 |
| ai_marketing | 3 | 营销策略泄露 |
| ai_sales | 3 | 线索评分/流失预测泄露 |
| ai_service | 5 | AI API Key 可被耗尽 + 泄露 |
| dashboard | 1 | 全公司统计数据泄露 |
| relationships | 3 | 客户关系数据裸奔 |
| service_tickets | 3 | 工单/SLA数据裸奔 |
| system | 8 | 数据字典CRUD无保护 |
| system_admin | 6 | 用户CRUD/RBAC管理裸奔 |

**合计: 10 模块, 36+ 端点, 0 认证**

---

## 其他发现

### [P1] ai_service.py — API Key 潜在泄露
```python
api_key = os.environ.get("DEEPSEEK_API_KEY", "")
```
未做掩码处理，日志中可能泄露。

### [P2] system_admin.py — 密码最低4位
```python
password: str = Field(..., min_length=4)
```
4位太弱，建议至少 8 位。

---

**结论: ❌ 不通过 — 必须为所有模块添加认证**
