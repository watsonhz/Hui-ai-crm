#!/bin/bash
# PostgreSQL backup with 7-day retention
BACKUP_DIR="./backups"
DB_NAME="${DB_NAME:-ai_crm}"
DB_USER="${DB_USER:-crm_user}"
DB_HOST="${DB_HOST:-localhost}"
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql.gz"

echo "[$(date)] Starting backup: $BACKUP_FILE"
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "[$(date)] Backup OK: $(du -h "$BACKUP_FILE" | cut -f1)"
    # Cleanup old backups
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "[$(date)] Cleaned backups older than $RETENTION_DAYS days"
else
    echo "[$(date)] Backup FAILED!"
    exit 1
fi
