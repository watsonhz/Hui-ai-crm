CREATE TABLE IF NOT EXISTS knowledge (
    id         BIGSERIAL PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    content    TEXT         NOT NULL,
    category   VARCHAR(50)  NOT NULL,
    tags       VARCHAR(500),
    source     VARCHAR(200),
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_knowledge_category ON knowledge(category);
