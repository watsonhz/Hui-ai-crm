-- 002-crm-core.sql: 招投标管理 / 项目管理 / 组织层级
CREATE TABLE IF NOT EXISTS bidding (
    id              BIGSERIAL PRIMARY KEY,
    title           VARCHAR(200)  NOT NULL,
    project_name    VARCHAR(200),
    bid_amount      NUMERIC(15,2),
    bid_status      SMALLINT      NOT NULL DEFAULT 1,
    bid_deadline    TIMESTAMPTZ,
    submit_deadline TIMESTAMPTZ,
    client_company  VARCHAR(200),
    client_contact  VARCHAR(100),
    description     TEXT,
    notes           TEXT,
    owner_id        BIGINT,
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);
COMMENT ON TABLE bidding IS '招投标管理';
COMMENT ON COLUMN bidding.bid_status IS '1=意向 2=招标中 3=投标中 4=评标中 5=中标 6=失标 7=废标 8=暂停 9=完成';

CREATE TABLE IF NOT EXISTS projects (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(200)  NOT NULL,
    description     TEXT,
    stage           SMALLINT      NOT NULL DEFAULT 1,
    start_date      DATE,
    end_date        DATE,
    budget          NUMERIC(15,2),
    actual_cost     NUMERIC(15,2),
    manager_id      BIGINT,
    org_id          BIGINT,
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);
COMMENT ON TABLE projects IS '项目管理';
COMMENT ON COLUMN projects.stage IS '1=线索..12=结项';

CREATE TABLE IF NOT EXISTS organizations (
    id              BIGSERIAL PRIMARY KEY,
    name            VARCHAR(200)  NOT NULL,
    parent_id       BIGINT        REFERENCES organizations(id),
    org_type        VARCHAR(20)   NOT NULL DEFAULT 'dept',
    description     TEXT,
    manager_id      BIGINT,
    sort_order      INT           NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);
COMMENT ON TABLE organizations IS '组织层级';
COMMENT ON COLUMN organizations.org_type IS 'company=公司 dept=部门 team=团队';

CREATE INDEX IF NOT EXISTS idx_bidding_status     ON bidding(bid_status)        WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_bidding_deadline    ON bidding(bid_deadline)      WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_projects_stage      ON projects(stage)            WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_organizations_parent ON organizations(parent_id)  WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_organizations_type   ON organizations(org_type)   WHERE deleted_at IS NULL;
