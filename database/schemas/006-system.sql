CREATE TABLE IF NOT EXISTS sys_dict_type (
    id         BIGSERIAL PRIMARY KEY,
    dict_name  VARCHAR(100) NOT NULL,
    dict_type  VARCHAR(100) NOT NULL UNIQUE,
    status     SMALLINT     DEFAULT 1,
    remark     VARCHAR(500),
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sys_dict_data (
    id         BIGSERIAL PRIMARY KEY,
    dict_type  VARCHAR(100) NOT NULL,
    dict_label VARCHAR(100) NOT NULL,
    dict_value VARCHAR(100) NOT NULL,
    sort_order SMALLINT     DEFAULT 0,
    status     SMALLINT     DEFAULT 1,
    remark     VARCHAR(500),
    css_class  VARCHAR(100),
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_dict_type ON sys_dict_data(dict_type);
