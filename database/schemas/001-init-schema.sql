-- AI-CRM Core Schema
-- Refer to docs/architecture/database-er.md

CREATE TABLE IF NOT EXISTS customers (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '客户名称',
    company VARCHAR(200) DEFAULT '' COMMENT '公司名称',
    industry VARCHAR(50) DEFAULT '' COMMENT '行业',
    phone VARCHAR(20) DEFAULT '' COMMENT '电话',
    email VARCHAR(100) DEFAULT '' COMMENT '邮箱',
    source VARCHAR(50) DEFAULT '' COMMENT '获客来源',
    level ENUM('A','B','C','D') NOT NULL DEFAULT 'C' COMMENT '客户等级',
    status ENUM('潜在','意向','谈判','成交','流失') NOT NULL DEFAULT '潜在' COMMENT '客户状态',
    owner_id BIGINT DEFAULT NULL COMMENT '负责人 ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted_at DATETIME DEFAULT NULL COMMENT '软删除时间',
    INDEX idx_status (status),
    INDEX idx_level (level),
    INDEX idx_created_at (created_at),
    INDEX idx_owner (owner_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户表';

CREATE TABLE IF NOT EXISTS sales_funnel (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL COMMENT '关联客户',
    stage ENUM('线索','初访','需求','报价','谈判','成交','丢单') NOT NULL DEFAULT '线索' COMMENT '阶段',
    amount DECIMAL(12,2) DEFAULT 0.00 COMMENT '预计金额',
    probability INT DEFAULT 0 COMMENT '成交概率(%)',
    expected_close DATE DEFAULT NULL COMMENT '预计成交日期',
    notes TEXT COMMENT '备注',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_customer (customer_id),
    INDEX idx_stage (stage),
    CONSTRAINT fk_funnel_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='销售漏斗表';

CREATE TABLE IF NOT EXISTS contacts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_id BIGINT NOT NULL COMMENT '关联客户',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    title VARCHAR(50) DEFAULT '' COMMENT '职位',
    phone VARCHAR(20) DEFAULT '' COMMENT '电话',
    email VARCHAR(100) DEFAULT '' COMMENT '邮箱',
    is_primary BOOLEAN DEFAULT FALSE COMMENT '是否主要联系人',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_customer (customer_id),
    CONSTRAINT fk_contact_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='联系人表';
