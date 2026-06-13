#!/bin/bash
#
# PC4 安全审查启动脚本 v3.1.0
# 用法: bash security/run-security-review.sh <PR_NUMBER|BRANCH_NAME>
#
# 此脚本执行以下操作:
# 1. 获取目标 PR/分支的代码变更
# 2. 将对抗性审查提示词与代码 diff 组合
# 3. 调用 Claude Code 进行安全审查
# 4. 将报告保存到 security/reports/
# 5. 将发现更新到 brain/learnings/adversarial-findings.jsonl
#

set -euo pipefail

PR="${1:-}"
if [ -z "$PR" ]; then
    echo "用法: bash security/run-security-review.sh <PR_NUMBER|BRANCH_NAME>"
    echo "示例: bash security/run-security-review.sh 42"
    echo "示例: bash security/run-security-review.sh feature/customer-api"
    exit 1
fi

TIMESTAMP=$(date -Iseconds)
SAFE_DATE=$(date -u +"%Y%m%dT%H%M%SZ")
REPORT_DIR="security/reports"
REPORT_FILE="${REPORT_DIR}/pc4-review-pr${PR}-${SAFE_DATE}.md"
PROMPT_FILE="security/cso-review-prompt.md"
FINDINGS_FILE="brain/learnings/adversarial-findings.jsonl"

# 确保目录存在
mkdir -p "${REPORT_DIR}"
mkdir -p "$(dirname "${FINDINGS_FILE}")"

echo "============================================"
echo "  PC4 对抗性安全审查引擎 v3.1.0"
echo "============================================"
echo ""
echo "审查时间: ${TIMESTAMP}"
echo "审查对象: PR/Branch #${PR}"
echo "提示词文件: ${PROMPT_FILE}"
echo "报告文件: ${REPORT_FILE}"
echo ""

# 获取当前分支名（用于 diff 基准）
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "HEAD")
BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")

# 尝试获取 PR 的 diff
echo "[1/5] 获取代码变更..."
DIFF_CONTENT=""

if git rev-parse --verify "origin/${PR}" >/dev/null 2>&1; then
    # PR 是一个远程分支名
    echo "  -> 检测到远程分支 origin/${PR}，获取与 ${BASE_BRANCH} 的差异..."
    git fetch origin "${PR}" 2>/dev/null || true
    DIFF_CONTENT=$(git diff "origin/${BASE_BRANCH}...origin/${PR}" 2>/dev/null || git diff "origin/${PR}" 2>/dev/null || echo "")
elif git rev-parse "${PR}" >/dev/null 2>&1; then
    # PR 是一个本地引用
    echo "  -> 检测到本地引用 ${PR}，获取与 ${BASE_BRANCH} 的差异..."
    DIFF_CONTENT=$(git diff "origin/${BASE_BRANCH}...${PR}" 2>/dev/null || git diff "${PR}" 2>/dev/null || echo "")
elif git rev-parse "origin/${PR}" >/dev/null 2>&1; then
    echo "  -> 检测到远程分支 origin/${PR}..."
    DIFF_CONTENT=$(git diff "origin/${BASE_BRANCH}...origin/${PR}" 2>/dev/null || echo "")
else
    # 假设 PR 是一个 PR 编号，尝试通过 GitHub CLI 获取
    echo "  -> 尝试通过 gh CLI 获取 PR #${PR} 的 diff..."
    if command -v gh &>/dev/null; then
        DIFF_CONTENT=$(gh pr diff "${PR}" 2>/dev/null || echo "")
    fi
    if [ -z "${DIFF_CONTENT}" ]; then
        echo "  -> 无法获取 PR diff，将审查当前工作目录与 ${BASE_BRANCH} 的差异"
        DIFF_CONTENT=$(git diff "origin/${BASE_BRANCH}...HEAD" 2>/dev/null || git diff HEAD 2>/dev/null || echo "")
    fi
fi

if [ -z "${DIFF_CONTENT}" ]; then
    echo "[WARN] 未能获取 diff 内容，将进行全量仓库审查"
    DIFF_CONTENT="[全量仓库审查] 审查整个代码仓库的安全状况"
fi

DIFF_SIZE=$(echo "${DIFF_CONTENT}" | wc -l)
echo "  -> Diff 大小: ${DIFF_SIZE} 行"

# 列出变更文件
echo ""
echo "[2/5] 变更文件清单..."
CHANGED_FILES=$(git diff --name-only "origin/${BASE_BRANCH}...HEAD" 2>/dev/null || git diff --name-only HEAD 2>/dev/null || echo "N/A")
echo "${CHANGED_FILES}" | head -50

# 组合提示词
echo ""
echo "[3/5] 组装审查提示词..."
REVIEW_CONTEXT="## 审查上下文

- **审查时间**: ${TIMESTAMP}
- **审查对象**: PR/Branch #${PR}
- **基准分支**: ${BASE_BRANCH}
- **变更文件数**: $(echo "${CHANGED_FILES}" | wc -l)
- **代码变更行数**: ${DIFF_SIZE}

## 变更文件列表

\`\`\`
${CHANGED_FILES}
\`\`\`

## 代码变更 (Diff)

\`\`\`diff
${DIFF_CONTENT}
\`\`\`

---

请对以上代码变更进行完整的对抗性安全审查，按照提示词中指定的格式输出审查报告。"

# 运行审查
echo "[4/5] 执行安全审查 (PC4)..."
echo "  -> 提示: 此过程可能需要几分钟，请耐心等待"
echo ""

# 将审查上下文与提示词结合
REVIEW_PROMPT=$(cat "${PROMPT_FILE}")
FULL_PROMPT="${REVIEW_PROMPT}

---

${REVIEW_CONTEXT}"

# 调用 Claude Code 进行审查
# 注意: claude 命令需要预先配置好认证和环境
if command -v claude &>/dev/null; then
    echo "${FULL_PROMPT}" | claude -p --output-format markdown > "${REPORT_FILE}" 2>&1 || {
        echo "[ERROR] Claude Code 执行失败，请检查配置"
        # 即使失败也保存上下文以便手动审查
        echo "${FULL_PROMPT}" > "${REPORT_DIR}/pc4-prompt-pr${PR}-${SAFE_DATE}.txt"
        echo "  -> 审查上下文已保存到 ${REPORT_DIR}/pc4-prompt-pr${PR}-${SAFE_DATE}.txt"
        exit 2
    }
else
    echo "[FATAL] 未找到 claude 命令。请先安装并配置 Claude Code CLI。"
    echo "  -> 审查提示词已保存到 ${REPORT_DIR}/pc4-prompt-pr${PR}-${SAFE_DATE}.txt"
    echo "${FULL_PROMPT}" > "${REPORT_DIR}/pc4-prompt-pr${PR}-${SAFE_DATE}.txt"
    exit 3
fi

# 记录发现到学习数据库
echo ""
echo "[5/5] 更新对抗性发现数据库..."

# 提取发现摘要（尝试从报告中解析 GO/NO-GO 和问题数量）
GO_NOGO=$(grep -i "APPROVED\|REJECTED\|CONDITIONAL" "${REPORT_FILE}" | head -1 || echo "UNKNOWN")
BLOCKING_COUNT=$(grep -c "BLOCKING" "${REPORT_FILE}" 2>/dev/null || echo "0")
NON_BLOCKING_COUNT=$(grep -c "NON_BLOCKING" "${REPORT_FILE}" 2>/dev/null || echo "0")

cat >> "${FINDINGS_FILE}" << FINDDOC
{"timestamp":"${TIMESTAMP}","pr":"${PR}","branch":"${CURRENT_BRANCH}","report":"${REPORT_FILE}","go_nogo":"${GO_NOGO}","blocking":${BLOCKING_COUNT},"non_blocking":${NON_BLOCKING_COUNT},"diff_size":${DIFF_SIZE}}
FINDDOC

echo ""
echo "============================================"
echo "  PC4 安全审查完成"
echo "============================================"
echo ""
echo "判定: ${GO_NOGO}"
echo "报告: ${REPORT_FILE}"
echo "发现问题: ${BLOCKING_COUNT} BLOCKING / ${NON_BLOCKING_COUNT} NON_BLOCKING"
echo "发现记录: ${FINDINGS_FILE}"
echo ""
echo "查看报告: cat ${REPORT_FILE}"
echo "============================================"
