# QA 设计文档一致性检查清单 (TASK-004)
#
# 用途：对照 docs/architecture/ 和 docs/api/ 建立功能验收矩阵
# 版本：v4.0
# 最后更新：2026-06-13

## 一、架构文档覆盖检查

| # | 文档 | 路径 | 状态 | 备注 |
|---|------|------|------|------|
| 1 | 系统架构设计 | docs/architecture/system-architecture.md | ✅ 已有 | v4.0，前后端分离 + 微服务 |
| 2 | 数据库 ER 图 | docs/architecture/database-er.md | ✅ 已有 | PostgreSQL + PGVector |
| 3 | API 规范 | docs/api/api-spec.md | ✅ 已有 | RESTful v4.0，78+ 端点 |

## 二、模块验收矩阵

### 基础业务模块（6个）

| # | 模块 | API 路径 | 文档状态 | 代码状态 | 测试状态 |
|---|------|----------|----------|----------|----------|
| 1 | 招投标管理 | /api/v1/bidding | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 2 | 项目管理 | /api/v1/projects | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 3 | 决策链 | /api/v1/decision-chain | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 4 | 关系维护 | /api/v1/relationships | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 5 | 验收管理 | /api/v1/acceptance | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 6 | 组织层级 | /api/v1/organizations | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |

### AI 赋能模块（7个）

| # | 模块 | API 路径 | 文档状态 | 代码状态 | 测试状态 |
|---|------|----------|----------|----------|----------|
| 7 | AI 诊断 | /api/v1/ai/diagnosis | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 8 | AI 报告 | /api/v1/ai/reports | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 9 | AI 客服 | /api/v1/ai/service | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 10 | AI 销售 | /api/v1/ai/sales | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 11 | AI 营销 | /api/v1/ai/marketing | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 12 | AI 运营 | /api/v1/ai/operations | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |

### 基础能力（3个）

| # | 模块 | API 路径 | 文档状态 | 代码状态 | 测试状态 |
|---|------|----------|----------|----------|----------|
| 13 | RAG 知识库 | /api/v1/knowledge | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 14 | 认证授权 | /api/v1/auth | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |
| 15 | 系统管理 | /api/v1/system | ✅ API 已定义 | ⬜ 待开发 | ⬜ 待测试 |

## 三、测试覆盖目标

| 层级 | 目标覆盖率 | 说明 |
|------|-----------|------|
| 单元测试 (unit/) | ≥ 85% | 核心业务逻辑 |
| 集成测试 (integration/) | ≥ 70% | 数据库 + Redis + 外部 API |
| API 测试 (api/) | ≥ 90% | 全部 78+ 端点 |
| 性能测试 (performance/) | P95 < 500ms | 并发 100 用户 |
| 安全测试 (security/) | OWASP Top 10 | SQL 注入 / XSS / CSRF / JWT |

## 四、测试环境配置

| 项目 | 值 |
|------|-----|
| API Base URL | http://192.168.0.170:8000/api/v1 |
| 测试数据库 | PostgreSQL 15+ (独立实例) |
| 测试 Redis | Redis 7.x (独立实例) |
| AI Mock | DeepSeek V4 API (sandbox 模式) |

## 五、QA 审查链位置

```
PC3 代码提交 → PC4 安全审查 → PC5 QA 测试（本节点）→ PC1 终审
                                  ↑
                              第二闸门（二级审查）
                              运行 /qa + /browse
```
