# AI-CRM 数据库设计（MySQL 8.0）

## 核心表结构

### customers（客户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键 |
| name | VARCHAR(100) | 客户名称 |
| company | VARCHAR(200) | 公司名称 |
| industry | VARCHAR(50) | 行业 |
| phone | VARCHAR(20) | 电话 |
| email | VARCHAR(100) | 邮箱 |
| source | VARCHAR(50) | 获客来源 |
| level | ENUM('A','B','C','D') | 客户等级 |
| status | ENUM('潜在','意向','谈判','成交','流失') | 状态 |
| owner_id | BIGINT FK | 负责人 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### sales_funnel（销售漏斗表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键 |
| customer_id | BIGINT FK | 关联客户 |
| stage | ENUM('线索','初访','需求','报价','谈判','成交','丢单') | 阶段 |
| amount | DECIMAL(12,2) | 预计金额 |
| probability | INT | 成交概率(%) |
| expected_close | DATE | 预计成交日期 |
| notes | TEXT | 备注 |

### contacts（联系人表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键 |
| customer_id | BIGINT FK | 关联客户 |
| name | VARCHAR(50) | 姓名 |
| title | VARCHAR(50) | 职位 |
| phone | VARCHAR(20) | 电话 |
| email | VARCHAR(100) | 邮箱 |
| is_primary | BOOLEAN | 是否主要联系人 |

