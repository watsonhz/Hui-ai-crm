-- 004-business-modules.sql: 决策链图谱 + 验收管理 + 关系维护
CREATE TABLE IF NOT EXISTS decision_chain (
    id            BIGSERIAL PRIMARY KEY,
    project_id    BIGINT       NOT NULL REFERENCES projects(id),
    name          VARCHAR(100) NOT NULL,
    role_type     VARCHAR(50)  NOT NULL,
    department    VARCHAR(100),
    weight        SMALLINT     NOT NULL DEFAULT 5,
    support_level SMALLINT     NOT NULL DEFAULT 0,
    contact_info  VARCHAR(200),
    notes         TEXT,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS acceptance (
    id              BIGSERIAL PRIMARY KEY,
    project_id      BIGINT       NOT NULL REFERENCES projects(id),
    title           VARCHAR(200) NOT NULL,
    acceptance_date DATE,
    status          SMALLINT     NOT NULL DEFAULT 1,
    result          TEXT,
    reviewer        VARCHAR(100),
    notes           TEXT,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS relationships (
    id                 BIGSERIAL PRIMARY KEY,
    customer_id        BIGINT       NOT NULL REFERENCES organizations(id),
    contact_name       VARCHAR(100) NOT NULL,
    contact_role       VARCHAR(50),
    relationship_level SMALLINT     NOT NULL DEFAULT 3,
    warmth             SMALLINT     DEFAULT 0,
    last_contact_date  TIMESTAMPTZ,
    notes              TEXT,
    created_at         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at         TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
