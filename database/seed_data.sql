-- 种子数据: 开发/测试环境初始化
-- 字典类型
INSERT INTO sys_dict_type (dict_name, dict_type, status) VALUES
    ('客户来源', 'customer_source', 1),
    ('客户行业', 'industry', 1),
    ('客户等级', 'customer_level', 1),
    ('投标状态', 'bid_status', 1),
    ('项目阶段', 'project_stage', 1),
    ('拜访方式', 'visit_type', 1),
    ('优先级', 'priority', 1),
    ('关系等级', 'relationship_level', 1),
    ('支持度', 'support_level', 1)
ON CONFLICT (dict_type) DO NOTHING;

-- 字典数据
INSERT INTO sys_dict_data (dict_type, dict_label, dict_value, sort_order, status) VALUES
    ('customer_source', '官网', 'website', 1, 1),
    ('customer_source', '展会', 'exhibition', 2, 1),
    ('customer_source', '转介绍', 'referral', 3, 1),
    ('customer_source', '电话营销', 'cold_call', 4, 1),
    ('industry', '政府', 'government', 1, 1),
    ('industry', '金融', 'finance', 2, 1),
    ('industry', '医疗', 'healthcare', 3, 1),
    ('industry', '教育', 'education', 4, 1),
    ('industry', '制造', 'manufacturing', 5, 1),
    ('customer_level', 'VIP', 'vip', 1, 1),
    ('customer_level', '重点', 'key', 2, 1),
    ('customer_level', '普通', 'normal', 3, 1),
    ('visit_type', '电话', 'phone', 1, 1),
    ('visit_type', '拜访', 'visit', 2, 1),
    ('visit_type', '会议', 'meeting', 3, 1),
    ('visit_type', '邮件', 'email', 4, 1),
    ('priority', 'P0紧急', 'P0', 1, 1),
    ('priority', 'P1重要', 'P1', 2, 1),
    ('priority', 'P2普通', 'P2', 3, 1)
ON CONFLICT DO NOTHING;

-- 组织示例数据
INSERT INTO organizations (id, name, parent_id, org_type, sort_order) VALUES
    (1, '总部', NULL, 'company', 0),
    (2, '销售部', 1, 'dept', 1),
    (3, '技术部', 1, 'dept', 2),
    (4, '财务部', 1, 'dept', 3),
    (5, '华东大区', 2, 'team', 1),
    (6, '华南大区', 2, 'team', 2)
ON CONFLICT DO NOTHING;

-- 演示项目
INSERT INTO projects (id, name, description, stage, budget, org_id) VALUES
    (1, '智慧城市项目', '某市政府数字化转型项目', 3, 5000000.00, 1),
    (2, '银行核心系统升级', '核心银行系统替换', 5, 8000000.00, 1),
    (3, '医院信息化平台', '三甲医院全院信息化建设', 8, 3000000.00, 1)
ON CONFLICT DO NOTHING;

-- 演示投标
INSERT INTO bidding (id, title, project_name, bid_amount, bid_status, client_company, description) VALUES
    (1, '智慧城市一期投标', '智慧城市项目', 4500000.00, 3, '某市人民政府', '智慧城市一期：政务云+大数据平台'),
    (2, '银行系统升级投标', '银行核心系统升级', 7500000.00, 5, '某商业银行', '核心银行系统替换：分布式架构迁移')
ON CONFLICT DO NOTHING;
