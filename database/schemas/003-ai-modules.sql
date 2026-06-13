-- 003-ai-modules.sql: AI 智能模块支撑表
CREATE TABLE IF NOT EXISTS sys_config (
    id           BIGSERIAL PRIMARY KEY,
    config_key   VARCHAR(100) NOT NULL UNIQUE,
    config_value TEXT         NOT NULL,
    description  VARCHAR(500),
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS crm_relationship (
    id            BIGSERIAL PRIMARY KEY,
    customer_id   BIGINT       NOT NULL REFERENCES organizations(id),
    contact_id    BIGINT,
    project_id    BIGINT       REFERENCES projects(id),
    visit_type    SMALLINT     NOT NULL DEFAULT 1,
    visit_date    TIMESTAMPTZ  NOT NULL,
    content       TEXT,
    outcome_level SMALLINT     DEFAULT 0,
    warmth_change SMALLINT     DEFAULT 0,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
COMMENT ON COLUMN crm_relationship.visit_type IS '1=电话 2=拜访 3=会议 4=邮件 5=微信';
COMMENT ON COLUMN crm_relationship.warmth_change IS '-2到+2 关系温度变化';

CREATE TABLE IF NOT EXISTS action_items (
    id          BIGSERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    priority    SMALLINT     NOT NULL DEFAULT 2,
    is_done     BOOLEAN      DEFAULT FALSE,
    due_date    TIMESTAMPTZ,
    assignee_id BIGINT,
    project_id  BIGINT       REFERENCES projects(id),
    customer_id BIGINT       REFERENCES organizations(id),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
COMMENT ON COLUMN action_items.priority IS '0=P0紧急 1=P1重要 2=P2普通';

CREATE TABLE IF NOT EXISTS ai_work_summary (
    id           BIGSERIAL PRIMARY KEY,
    report_type  VARCHAR(20)  NOT NULL,
    title        VARCHAR(200) NOT NULL,
    content      TEXT         NOT NULL,
    period_start TIMESTAMPTZ,
    period_end   TIMESTAMPTZ,
    is_edited    TEXT         DEFAULT '0',
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
COMMENT ON COLUMN ai_work_summary.report_type IS 'daily/weekly/monthly';

-- 默认阈值配置
INSERT INTO sys_config (config_key, config_value, description) VALUES
    ('s1_visit_overdue_days',  '{"vip":7,"key":14,"normal":30}', 'S1拜访超期天数阈值(按客户等级)'),
    ('s2_stage_stall_days',     '{"default":14}', 'S2项目阶段卡顿阈值'),
    ('s4_p0_overdue_count',     '2', 'S4 P0待办逾期数量阈值'),
    ('s5_warmth_drop_count',    '2', 'S5关键人关系恶化连续降温次数'),
    ('s5_warmth_min_weight',    '5', 'S5关键人关系恶化最小权重'),
    ('s7_keyperson_silence_days','21', 'S7关键人长期未接触天数'),
    ('s7_keyperson_min_weight', '7', 'S7关键人长期未接触最小权重'),
    ('s9_low_outcome_count',    '2', 'S9拜访产出低下连续次数'),
    ('s11_acceptance_overdue_days','7', 'S11验收逾期天数'),
    ('s12_payment_delay_days',  '30', 'S12回款延迟天数')
ON CONFLICT (config_key) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_rel_customer    ON crm_relationship(customer_id);
CREATE INDEX IF NOT EXISTS idx_rel_project     ON crm_relationship(project_id);
CREATE INDEX IF NOT EXISTS idx_rel_visit_date  ON crm_relationship(visit_date);
CREATE INDEX IF NOT EXISTS idx_action_due      ON action_items(due_date) WHERE is_done = FALSE;
CREATE INDEX IF NOT EXISTS idx_action_project  ON action_items(project_id);
