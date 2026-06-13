#!/bin/bash
# PC1 自动进度检查脚本 — 检查所有节点的 git 提交和代码产出
# 用法: bash scripts/check-progress.sh

REPORT="D:/DevProjects/ai-crm/security/audit-reports/progress-$(date +%Y%m%d-%H%M).txt"
echo "==========================================" | tee -a "$REPORT"
echo "  5机集群进度报告 - $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$REPORT"
echo "==========================================" | tee -a "$REPORT"

check_pc() {
    local name=$1
    local host=$2
    local path=$3
    local task=$4
    echo "" | tee -a "$REPORT"
    echo "--- $name ---" | tee -a "$REPORT"

    result=$(ssh -o ConnectTimeout=8 -o StrictHostKeyChecking=no "$host" "cd $path 2>/dev/null && echo 'BRANCH:' && git branch --show-current 2>/dev/null && echo 'COMMITS:' && git log --oneline -5 2>/dev/null && echo 'STATUS:' && git status --short 2>/dev/null | head -10 && echo 'FILES:' && find . -name '*.py' -o -name '*.vue' -o -name '*.ts' 2>/dev/null | grep -v node_modules | grep -v '.git/' | wc -l | xargs -I{} echo '{} source files'" 2>&1)

    echo "$result" | tee -a "$REPORT"

    # Check for uncommitted changes
    if echo "$result" | grep -q "^?\|^ M\|^ D\|^ A"; then
        echo "  ⚠️  $name: Uncommitted changes!" | tee -a "$REPORT"
    fi

    # Check for new commits today
    today=$(date +%Y-%m-%d)
    if echo "$result" | grep -q "$today"; then
        echo "  ✅ $name: Commits today" | tee -a "$REPORT"
    else
        echo "  ⏳ $name: No commits today" | tee -a "$REPORT"
    fi
}

# Check all PCs
check_pc "PC2 (前端)" "pc2" "C:/DevProjects/ai-crm" "TASK-002"
check_pc "PC3 (后端)" "pc3" "~/DevProjects/ai-crm" "TASK-001"
check_pc "PC4 (安全)" "pc4" "C:/DevProjects/ai-crm" "TASK-003"
check_pc "PC5 (测试)" "pc5" "C:/DevProjects/ai-crm" "TASK-004"

echo "" | tee -a "$REPORT"
echo "==========================================" | tee -a "$REPORT"
echo "  报告保存至: $REPORT" | tee -a "$REPORT"
echo "==========================================" | tee -a "$REPORT"
