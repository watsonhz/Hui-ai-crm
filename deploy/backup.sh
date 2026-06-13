#!/bin/bash
# 数据库备份脚本
set -e
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-postgres}"
DB_PASS="${DB_PASS:-Admin@90088*}"
DB_NAME="${DB_NAME:-ai_crm}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$BACKUP_DIR"
export PGPASSWORD="$DB_PASS"
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -Fc -f "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"
echo "Backup saved: $BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.dump"
# 保留最近7天
find "$BACKUP_DIR" -name "${DB_NAME}_*.dump" -mtime +7 -delete
