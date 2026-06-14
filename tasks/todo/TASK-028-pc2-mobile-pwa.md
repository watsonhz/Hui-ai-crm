---
task_id: TASK-028
title: 移动端PWA适配 + 离线访问 + 推送通知
assignee: pc2
role: frontend-developer
priority: P0
deadline: 2026-06-30
branch: feature/TASK-028-mobile-pwa
dependencies: [TASK-026]
tags: [v1.1, pwa, mobile, responsive, push]
---

# TASK-028：移动端PWA

## Part A: PWA 配置
- manifest.json（应用名/图标/主题色/全屏）
- Service Worker（离线缓存策略）
- 安装提示（Add to Home Screen）
- 离线页面

## Part B: 移动端深度适配
- 底部Tab导航（移动端替代侧边栏）
- 卡片式布局优化
- 触摸手势支持（滑动/长按）
- 移动端表单优化（日期选择/下拉）

## Part C: 推送通知
- Web Push API 集成
- PC1任务下发推送
- PC4/PC5审查结果推送

## 验收标准
- [ ] PWA可安装到主屏幕
- [ ] 离线访问已缓存页面
- [ ] 移动端12+页面无溢出
- [ ] Lighthouse PWA评分 > 90

完成后: git commit/push, 移至 tasks/done/
