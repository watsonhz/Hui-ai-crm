---
task_id: TASK-026
title: 数据导出(Excel/PDF) + 消息通知中心 + 文件附件管理
assignee: pc2
role: frontend-developer
priority: P1
deadline: 2026-06-26
branch: feature/TASK-026-export-notify
dependencies: [TASK-022]
tags: [sprint7, vue3, export, notification, upload]
---

# TASK-026：数据导出 + 通知 + 附件

## Part A: 数据导出
- 客户列表导出 Excel（xlsx）
- 报表导出 PDF
- 投标数据导出 CSV
- 导出按钮带加载态 + 进度提示

## Part B: 消息通知中心
- 顶部铃铛下拉：未读消息列表
- WebSocket 实时推送（PC1 任务下发 / PC4 审查结果 / PC5 QA 报告）
- 通知分类：系统/任务/审查/QA
- 已读/未读状态 + 全部标为已读

## Part C: 文件附件管理
- 客户附件上传（合同/方案/截图）
- 支持拖拽上传 + 多文件
- 预览：图片/PDF
- 上传进度条

## 验收标准
- [ ] Excel/PDF/CSV 导出均可下载
- [ ] 通知中心实时更新
- [ ] 文件上传+预览正常
- [ ] 响应式适配

完成后: git commit/push, 移至 tasks/done/
