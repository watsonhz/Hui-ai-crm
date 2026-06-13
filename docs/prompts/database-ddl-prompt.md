# 数据库DDL生成 Prompt

请根据以下数据模型设计，生成 PostgreSQL 15+ 的 DDL 脚本：
1. 表名使用小写+下划线命名
2. 所有表包含 id BIGSERIAL PRIMARY KEY
3. 所有表包含 created_at TIMESTAMP DEFAULT NOW()
4. 所有表包含 updated_at TIMESTAMP DEFAULT NOW()
5. 外键约束使用 ON DELETE SET NULL
6. 索引：外键字段 + 常用查询字段
7. 注释使用 COMMENT ON 语法
8. PGVector 向量字段使用 vector(1536) 类型
