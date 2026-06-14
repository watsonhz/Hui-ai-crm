CREATE TABLE IF NOT EXISTS users (
    id            BIGSERIAL PRIMARY KEY,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email         VARCHAR(100),
    full_name     VARCHAR(100),
    role          VARCHAR(20)  NOT NULL DEFAULT 'sales',
    is_active     BOOLEAN      DEFAULT TRUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- 默认管理员
INSERT INTO users (username, password_hash, email, full_name, role) VALUES
    ('admin', '$2b$12$LJ3m4ys3GZfnYMz8kVsKaOGFqOLqXaCLaYVYgYKx0cB3FqvnkKFru', 'admin@aicrm.local', '系统管理员', 'admin')
ON CONFLICT (username) DO NOTHING;
