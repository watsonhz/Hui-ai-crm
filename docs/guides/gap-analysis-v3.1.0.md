# Gap Analysis — 对照 v3.1.0 指南检查结果

**检查人**: PC1 (CEO) | **日期**: 2026-06-13
**指南**: AI开发团队从0到1搭建指南-v3.1.0-5机版-更新.docx

## IP 分配 (Section 2.3)

| PC | IP | OS | 角色 |
|----|-----|-----|------|
| PC1 | 192.168.0.168 | WIN11 | CEO + OpenClaw 指挥 |
| PC2 | 192.168.0.169 | WIN11 | PM + 前端 + UI/UX |
| PC3 | 192.168.0.170 | macOS | 后端架构师 + DevOps |
| PC4 | 192.168.0.171 | Windows 11 | 安全审查 + 文档 + 对抗性审查 |
| PC5 | 192.168.0.253 | WinServer2019 | QA 测试专机 |

---

## 🚨 需要修复

### P0 — IP 地址错误

| 文件 | 行 | 错误 | 正确 |
|------|-----|------|------|
| `backend/.env.example` | CORS_ORIGINS | `192.168.0.170:3000` | `192.168.0.169:3000` |
| `backend/app/core/config.py` | CORS_ORIGINS 默认值 | 只有 `localhost:3000` | 增加 `192.168.0.169:3000` |

> PC2 前端在 .169，不是 .170。.170 是 PC3 后端的 IP。

### P1 — Git 分支命名不一致
- **指南**: `feat/*` (feat/TASK-001-xxx)
- **当前**: `feature/*` (feature/TASK-001-customer-crud)
- **影响**: TASK-001, TASK-002 的 `branch:` 字段

### P1 — 调度脚本用主机名而非 IP
- **当前**: SSH 主机名 `pc2`, `pc3`, `pc4`, `pc5`（需配置 DNS/hosts）
- **指南**: 直接使用 IP 地址
- **建议**: 脚本内维护 IP 映射

### P1 — 缺少 PC4 + PC5 任务
v3.1.0 是三闸门审查链（PC4 安全 → PC5 QA → PC1 终审），当前只有 PC3 和 PC2 的任务。

### P2 — 架构图缺少 PC4/PC5
`system-architecture.md` 的 ASCII 图只显示 PC1/PC2/PC3，未体现审查链。

### P2 — 缺少 brain/ 知识库
指南第12章指定了 `brain/` 目录，但未创建。

---

## ✅ 已正确实现

| 检查项 | 状态 |
|--------|------|
| 技术选型 (FastAPI + React + MySQL + Redis) | ✅ 匹配 |
| API Base URL (192.168.0.170:8000) | ✅ PC3 正确 |
| 数据库表设计 (customers, sales_funnel, contacts) | ✅ 匹配 |
| Docker Compose (MySQL + Redis) | ✅ 匹配 |
| 响应格式 {code, message, data} | ✅ 匹配 |
| 前端 Vite + React + MUI | ✅ 匹配 |
| MSW Mock 策略 | ✅ 超越指南（v3.1.0 未详述前端独立开发） |
| .gitignore | ✅ |
| PC2 Windows 路径, PC3 Unix 路径 | ✅ |
