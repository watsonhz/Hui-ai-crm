---
task_id: TASK-017
title: AI销售支持+营销推广 + 系统管理API(RBAC)
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-17
branch: feature/TASK-017-ai-sales-system
dependencies: [TASK-013]
tags: [sprint5, ai-sales, ai-marketing, rbac, system]
---

# TASK-017：AI销售支持+营销推广 + 系统管理API

## Part A: AI销售支持 (/api/v1/ai/sales)
- POST /lead-scoring — 线索评分
- POST /churn-prediction — 客户流失预测
- GET  /upsell-opportunities/{customer_id} — 交叉销售机会
- GET  /sales-forecast — 销售预测(季度)

## Part B: AI营销推广 (/api/v1/ai/marketing)
- POST /campaign-recommend — 营销活动推荐
- POST /content-generate — AI营销内容生成
- GET  /roi-analysis — 营销ROI分析

## Part C: 系统管理API (/api/v1/system)
- 用户管理: CRUD + 状态/锁定
- 角色管理: 11个预置角色CRUD
- 权限管理: 权限树+角色分配
- 操作日志: 分页查询+筛选
- 系统配置: 键值对管理

## 验收标准
- [ ] AI销售4端点可用
- [ ] AI营销3端点可用
- [ ] RBAC用户/角色/权限完整
- [ ] 操作日志记录
- [ ] pytest > 80%

完成后: git commit, 移至 tasks/done/
