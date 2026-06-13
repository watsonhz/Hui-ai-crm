---
task_id: TASK-004
title: PC5 QA 测试框架 + 自动化回归
assignee: pc5
role: qa-engineer
priority: P0 (最高)
deadline: 2026-06-11
branch: feat/TASK-004-qa-framework
dependencies: [TASK-001]
tags: [qa, playwright, k6, newman, regression]
---

# TASK-004：PC5 QA 测试框架 + 自动化回归

## 需求描述
PC5 作为 QA 测试闸门（v3.1.0 第二闸），在 PC4 安全审查通过后执行功能 + 性能 + 回归测试。

## 测试维度（按 v3.1.0 9.2 节）
1. **功能正确性**: API 业务逻辑验证
2. **边界测试**: 空值/极值/并发冲突
3. **性能基准**: P50/P95/P99 延迟 + 内存泄漏
4. **跨平台**: Windows Server 2019 + macOS + Windows 11 + Edge
5. **回归测试**: 每日凌晨 3:00 自动执行

## 技术规范
- 主机: Windows Server 2019 @ 192.168.0.253
- 仓库路径: D:/DevProjects/ai-crm
- 测试工具: Playwright (E2E) + k6 (性能) + Newman (API)
- 报告: IIS 托管 http://192.168.0.253:8080/qa-reports/

## CLI 命令
```
claude -p "/qa"              # 全量测试
claude -p "/qa-only"         # 仅测试模式
claude -p "/browse <场景>"    # 浏览器自动化
claude -p "/benchmark"       # 性能基准
```

## 验收标准
- [ ] Playwright 安装配置完成 (5 浏览器 project)
- [ ] k6 / Newman 安装配置完成
- [ ] QA 报告发布到 IIS (http://192.168.0.253:8080)
- [ ] 对 TASK-001 API 执行完整 QA: 0 P0/P1 Bug
- [ ] Windows 计划任务：每日凌晨 3:00 自动回归
- [ ] QA 报告格式: 通过/失败 + 截图 + 执行时长 + 历史趋势

## 完成标记
完成后将本文件移至 tasks/done/ 并创建 TASK-004-done.md
