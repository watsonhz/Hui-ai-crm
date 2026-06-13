---
task_id: TASK-009
title: AI工作报告生成 + RAG知识库 (PGVector)
assignee: pc3
role: backend-architect
priority: P0
deadline: 2026-06-15
branch: feature/TASK-009-ai-reports-rag
dependencies: [TASK-005]
tags: [sprint3, ai, reports, rag, pgvector]
---

# TASK-009：AI工作报告生成 + RAG知识库

## Part A: AI工作报告自动生成
文件: backend/app/services/report_generator.py

日报 (daily_report):
- 数据源：当日拜访纪要 + 行动项完成状态
- 模板：今日工作/完成事项/存在问题/明日计划

周报 (weekly_report):
- 数据源：本周5份日报 + 统计汇总
- 模板：本周总结/客户进展/风险预警/下周计划

月报 (monthly_report):
- 数据源：本月4份周报 + 业绩数据
- 模板：业绩概览/重点项目/丢单分析/团队效能/下月预测

API端点:
- POST /api/v1/ai/reports/daily
- POST /api/v1/ai/reports/weekly
- POST /api/v1/ai/reports/monthly
- GET  /api/v1/ai/reports/{id}

## Part B: RAG知识库 (PGVector)
文件: backend/app/services/vector_service.py

- 文档向量化 (text-embedding-3-small, 1536维)
- PGVector 存储与检索
- POST /api/v1/knowledge/documents — 上传文档
- GET  /api/v1/knowledge/search?q= — 语义搜索

## 验收标准
- [ ] 3种报告生成可用
- [ ] RAG 文档上传+搜索可用
- [ ] PGVector 向量检索 < 500ms
- [ ] pytest 测试 > 80%

完成后: git commit/push, 移至 tasks/done/
