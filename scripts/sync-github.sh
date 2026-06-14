#!/bin/bash
# Auto-sync: Pull from PC2/PC4/PC5 and push to GitHub
# Runs every 10 minutes via cron

REPO="d:/DevProjects/ai-crm"
LOG="$REPO/security/audit-reports/sync-log.txt"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') ===" >> "$LOG"

sync_pc() {
    local name=$1 host=$2 path=$3
    echo "[$name] Checking..." >> "$LOG"
    
    # Check for new commits since last sync
    LAST=$(cat "$REPO/.sync-$name" 2>/dev/null || echo "HEAD")
    
    result=$(ssh -o ConnectTimeout=8 -o StrictHostKeyChecking=no "$host" \
        "cd $path 2>/dev/null && git log --oneline -5" 2>/dev/null)
    
    if [ -n "$result" ]; then
        LATEST=$(echo "$result" | head -1 | awk '{print $1}')
        if [ "$LATEST" != "$LAST" ]; then
            echo "[$name] NEW commits found!" >> "$LOG"
            echo "$result" >> "$LOG"
            
            # Pull via bundle+fetch
            ssh "$host" "cd $path && git bundle create /tmp/sync-$name.bundle HEAD~5..HEAD" 2>/dev/null
            scp "$host:/tmp/sync-$name.bundle" "$REPO/.sync-$name.bundle" 2>/dev/null
            
            if [ -f "$REPO/.sync-$name.bundle" ]; then
                cd "$REPO"
                git fetch ".sync-$name.bundle" 2>/dev/null && \
                git merge FETCH_HEAD --no-ff -m "sync: $name auto-merge $(date +%Y%m%d-%H%M)" 2>/dev/null
                git push github main develop 2>/dev/null
                echo "$LATEST" > "$REPO/.sync-$name"
                echo "[$name] Synced to GitHub" >> "$LOG"
            fi
        else
            echo "[$name] No new commits" >> "$LOG"
        fi
    fi
}

sync_pc "PC2" "pc2" "C:/DevProjects/ai-crm"
sync_pc "PC4" "pc4" "C:/DevProjects/ai-crm"  
sync_pc "PC5" "pc5" "C:/DevProjects/ai-crm"

echo "" >> "$LOG"
