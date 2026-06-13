# API 设计 Prompt

请设计以下功能的 RESTful API。要求：
1. 遵循项目统一响应格式：{ "code": 200, "message": "success", "data": {...} }
2. 包含完整的 Pydantic Schema（请求/响应）
3. 参数校验规则
4. 分页参数（page, page_size）
5. 排序参数（sort_by, sort_order）
6. 认证要求（JWT Bearer Token）
7. 速率限制建议
