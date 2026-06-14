---
task_id: TASK-027
title: 生产环境部署 + Docker Compose + 监控告警
assignee: pc3
role: devops-engineer
priority: P1
deadline: 2026-06-28
branch: feature/TASK-027-deploy
dependencies: [TASK-025]
tags: [sprint7, docker, deploy, monitoring, production]
---

# TASK-027：生产环境部署

## Part A: Docker Compose 生产配置
- docker-compose.prod.yml：PostgreSQL + Redis + Backend + Frontend + Nginx
- Nginx 反向代理（前端 :80，后端 :8000 → /api）
- 环境变量管理（.env.prod）
- 健康检查 + 自动重启

## Part B: 数据库备份
- PostgreSQL 自动备份脚本（每日）
- 备份保留策略（7天滚动）
- 恢复测试流程

## Part C: 监控告警
- Prometheus + Grafana（可选）
- 健康检查端点监控
- 飞书 Webhook 告警（服务宕机/磁盘满/证书到期）

## 验收标准
- [ ] `docker compose up -d` 一键启动全栈
- [ ] Nginx 反向代理正确
- [ ] 备份脚本可执行
- [ ] 健康检查自动告警

完成后: git commit/push, 移至 tasks/done/
