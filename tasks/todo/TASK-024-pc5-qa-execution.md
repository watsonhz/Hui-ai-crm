---
task_id: TASK-024
title: PC5 QA完整回归测试 + 性能基准 + IIS报告发布
assignee: pc5
role: qa-engineer
priority: P0
deadline: 2026-06-22
branch: feature/TASK-024-qa-execution
dependencies: [TASK-023]
tags: [sprint6, qa, regression, performance, iis]
---

# TASK-024：PC5 QA完整回归测试

## 需求描述
在 PC5 (Windows Server 2019) 上执行完整的 QA 回归测试套件。

## 测试维度
1. Newman API 全量测试 (7+ 条断言覆盖所有端点)
2. Playwright E2E (5 浏览器，10+ 用例)
3. k6 性能基准 (P50/P95/P99 延迟)
4. 跨平台兼容性 (Win11/macOS/WinServer2019 + Chrome/Edge/Safari/Firefox)

## QA 报告
- 通过/失败 + 截图 + 执行时长
- 与上一版本性能趋势对比
- 发布到 IIS: http://192.168.0.253:8080/qa-reports/
- 注册 Windows 计划任务：每日凌晨 3:00 自动回归

## 验收标准
- [ ] Newman 0 failures
- [ ] Playwright 10+ 用例全部通过
- [ ] k6 P95 < 500ms
- [ ] QA 报告可通过浏览器访问
- [ ] 计划任务注册成功

完成后: git commit, 移至 tasks/done/
