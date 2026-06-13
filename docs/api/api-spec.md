# AI-CRM RESTful API 规范

## 基础信息
- Base URL: http://192.168.0.170:8000/api/v1
- 认证方式: Bearer Token (JWT)
- 请求格式: JSON
- 响应格式: { "code": 200, "message": "success", "data": {...} }

## 客户管理 API
| 方法 | 路径 | 说明 | 负责人 |
|------|------|------|--------|
| POST | /customers | 创建客户 | PC3 |
| GET | /customers | 客户列表(分页) | PC3 |
| GET | /customers/{id} | 客户详情 | PC3 |
| PUT | /customers/{id} | 更新客户 | PC3 |
| DELETE | /customers/{id} | 删除客户(软删除) | PC3 |
| GET | /customers/search | 全文搜索 | PC3 |

## 销售漏斗 API
| 方法 | 路径 | 说明 | 负责人 |
|------|------|------|--------|
| POST | /funnel/opportunities | 创建商机 | PC3 |
| GET | /funnel/opportunities | 商机列表 | PC3 |
| PUT | /funnel/opportunities/{id}/stage | 推进阶段 | PC3 |
| GET | /funnel/statistics | 漏斗统计 | PC3 |

## AI 智能 API
| 方法 | 路径 | 说明 | 负责人 |
|------|------|------|--------|
| POST | /ai/recommend | AI 推荐相似客户 | PC3 |
| GET | /ai/customer-profile/{id} | 客户画像分析 | PC3 |
| POST | /ai/lead-scoring | 线索评分 | PC3 |
| GET | /ai/sales-prediction | 销售预测 | PC3 |

## 数据分析 API
| 方法 | 路径 | 说明 | 负责人 |
|------|------|------|--------|
| GET | /analytics/dashboard | 仪表盘数据 | PC3 |
| GET | /analytics/sales-trend | 销售趋势 | PC3 |
| GET | /analytics/conversion-rate | 转化率 | PC3 |
| GET | /analytics/export | 数据导出 | PC3 |
