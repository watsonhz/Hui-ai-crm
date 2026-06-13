# AI-CRM RESTful API 规范 (v4.0)

## 基础信息
- Base URL: http://192.168.0.170:8000/api/v1
- 认证方式: Bearer Token (JWT) / 微信扫码 / 短信验证码
- 请求格式: JSON
- 响应格式: { "code": 200, "message": "success", "data": {...} }

## 错误码
| Code | 说明 |
|------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证（JWT过期/无效） |
| 403 | 无权限（角色不匹配） |
| 404 | 资源不存在 |
| 422 | 参数校验失败 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |

## 核心API模块（78+端点）

### 基础业务模块
| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| 招投标管理 | /api/v1/bidding | 9态状态机 |
| 项目管理 | /api/v1/projects | 12阶段流转 |
| 决策链 | /api/v1/decision-chain | 图谱+三层关系 |
| 关系维护 | /api/v1/relationships | 5次拜访+纪要 |
| 验收管理 | /api/v1/acceptance | 分阶段验收+回款 |
| 组织层级 | /api/v1/organizations | 树形结构+分层 |

### AI赋能模块
| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| AI诊断 | /api/v1/ai/diagnosis | 12信号引擎 |
| AI报告 | /api/v1/ai/reports | 日报/周报/月报 |
| AI客服 | /api/v1/ai/service | 工单+SLA |
| AI销售 | /api/v1/ai/sales | 销售支持 |
| AI营销 | /api/v1/ai/marketing | 营销推广 |
| AI运营 | /api/v1/ai/operations | 运营管理 |

### 基础能力
| 模块 | 路径前缀 | 说明 |
|------|----------|------|
| RAG知识库 | /api/v1/knowledge | 向量检索 |
| 认证授权 | /api/v1/auth | JWT+RBAC |
| 系统管理 | /api/v1/system | 用户/角色/配置/日志 |

## 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 分页参数
- page: 页码 (默认1)
- page_size: 每页数量 (默认20, 最大100)
- sort_by: 排序字段
- sort_order: asc/desc
