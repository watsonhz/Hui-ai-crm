# AI-CRM v4.0 - 企业级政企大B客户管理系统

## 项目结构

```
Hui-crm/
├── backend/           # FastAPI + SQLAlchemy 2.0 + PostgreSQL
│   ├── app/
│   │   ├── api/v1/    # 12个路由模块 50+ API端点
│   │   ├── models/    # 14张数据表 SQLAlchemy ORM
│   │   ├── schemas/   # Pydantic 请求/响应校验
│   │   ├── services/  # AI诊断引擎 + 报告生成器
│   │   ├── core/      # 数据库连接 + JWT安全模块
│   │   └── middleware/ # JWT中间件
│   ├── tests/         # 91个测试 88%覆盖率
│   └── docs/prompts/  # AI报告Prompt模板
├── frontend/          # React 18 + TypeScript + Ant Design 5
│   └── src/
│       ├── pages/     # 11个页面
│       ├── components/ # AuthGuard
│       ├── api/       # Axios客户端
│       ├── stores/    # Zustand状态管理
│       └── router/    # React Router 6
├── database/
│   ├── schemas/       # 8个DDL脚本
│   └── seed_data.sql  # 种子数据
├── deploy/
│   ├── docker-compose.yml           # 开发环境
│   ├── docker-compose.full.yml      # 生产环境
│   ├── Dockerfile.frontend          # 前端镜像
│   └── nginx.conf                   # Nginx配置
└── Makefile           # 开发/测试/部署命令
```

## 快速启动

```bash
# 1. 启动基础设施
make up

# 2. 初始化数据库
make db-init
make db-seed

# 3. 启动后端 (http://localhost:8000/docs)
make api

# 4. 启动前端 (http://localhost:5173)
cd frontend && npm install && npm run dev

# 5. 运行测试
make test
```

## 生产部署

```bash
make deploy        # 启动全栈 (PostgreSQL + Redis + 后端 + Nginx前端)
make deploy-down   # 停止
```

## API 模块

| 模块 | 前缀 | 说明 |
|------|------|------|
| 招投标管理 | /api/v1/bidding | 9态状态机 + 日历 |
| 项目管理 | /api/v1/projects | 12阶段 + 看板 |
| 组织层级 | /api/v1/organizations | 树形结构 |
| 决策链图谱 | /api/v1/decision-chain | 关键人+权重 |
| 验收管理 | /api/v1/acceptance | 验收跟踪 |
| 关系维护 | /api/v1/relationships | 客户关系 |
| AI诊断报告 | /api/v1/ai | 12信号引擎 + 日报/周报/月报 |
| 认证授权 | /api/v1/auth | JWT登录注册 |
| 系统管理 | /api/v1/system | 数据字典 |
| 知识库 | /api/v1/knowledge | RAG检索 |
| 数据看板 | /api/v1/dashboard | 聚合统计 |

## 技术栈

- **后端**: Python 3.12 / FastAPI / SQLAlchemy 2.0 / PostgreSQL 15 + PGVector / Redis 7
- **前端**: React 18 / TypeScript / Ant Design 5 / Zustand / Vite 5
- **AI**: DeepSeek V4 / 12信号检测 / Prompt模板引擎
- **基础设施**: Docker Compose / Nginx / Colima (macOS)
# Hui-ai-crm
