# PC4 对抗性安全审查启动脚本 v3.1.0 (Windows PowerShell)
# 用法: .\security\run-adversarial-review.ps1 -PR "42"
#        .\security\run-adversarial-review.ps1 -PR "feature/TASK-001-crm-core-api"

param(
    [Parameter(Mandatory=$true, HelpMessage="PR 编号或分支名称")]
    [string]$PR
)

$ErrorActionPreference = "Stop"
$timestamp = Get-Date -Format "yyyy-MM-ddTHHmmssZ"
$reportDir = "security\reports"
$reportFile = "${reportDir}\pc4-review-${PR}-${timestamp}.md"
$promptFile = "security\cso-review-prompt.md"
$findingsFile = "brain\learnings\adversarial-findings.jsonl"
$templateFile = "security\review-report-template.md"

# 确保目录存在
if (-not (Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
}
$findingsDir = Split-Path $findingsFile -Parent
if (-not (Test-Path $findingsDir)) {
    New-Item -ItemType Directory -Path $findingsDir -Force | Out-Null
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PC4 对抗性安全审查引擎 v3.1.0" -ForegroundColor Cyan
Write-Host "  Windows PowerShell Edition" -ForegroundColor DarkCyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "审查时间: $timestamp"
Write-Host "审查对象: PR/Branch #$PR"
Write-Host "提示词文件: $promptFile"
Write-Host "报告文件: $reportFile"
Write-Host "报告模板: $templateFile"
Write-Host ""

# ──────────────────────────── 步骤 1: 获取代码变更 ────────────────────────────
Write-Host "[1/5] 获取代码变更..." -ForegroundColor Yellow

$baseBranch = "main"
try {
    $baseBranch = git symbolic-ref refs/remotes/origin/HEAD 2>$null
    if ($baseBranch) {
        $baseBranch = $baseBranch -replace '^refs/remotes/origin/', ''
    } else {
        $baseBranch = "main"
    }
} catch {
    $baseBranch = "main"
}

$diffContent = ""

# 尝试多种方式获取 diff
try {
    # 尝试作为远程分支
    git fetch origin $PR 2>$null | Out-Null
    $diffContent = git diff "origin/${baseBranch}...origin/${PR}" 2>$null
    if (-not $diffContent) {
        # 尝试作为本地引用
        $diffContent = git diff "origin/${baseBranch}...${PR}" 2>$null
    }
} catch {
    # 尝试 gh CLI
    try {
        $diffContent = gh pr diff $PR 2>$null
    } catch {
        # 默认: 当前 HEAD 与 main 的差异
        $diffContent = git diff "origin/${baseBranch}...HEAD" 2>$null
    }
}

if (-not $diffContent) {
    Write-Host "  [WARN] 未能获取 diff，将进行全量仓库审查" -ForegroundColor DarkYellow
    $diffContent = "[全量仓库审查] 审查整个代码仓库的安全状况"
}

$diffLines = ($diffContent | Measure-Object -Line).Lines
Write-Host "  -> Diff 大小: $diffLines 行" -ForegroundColor Gray

# ──────────────────────────── 步骤 2: 变更文件清单 ────────────────────────────
Write-Host ""
Write-Host "[2/5] 变更文件清单..." -ForegroundColor Yellow

$changedFiles = git diff --name-only "origin/${baseBranch}...HEAD" 2>$null
if (-not $changedFiles) {
    $changedFiles = "N/A (全量审查)"
}
Write-Host $changedFiles
$changedFileCount = ($changedFiles | Measure-Object -Line).Lines

# ──────────────────────────── 步骤 3: 获取对抗性审查清单 ────────────────────────────
Write-Host ""
Write-Host "[3/5] 加载 TASK-001 对抗性审查清单..." -ForegroundColor Yellow

$checklistContent = ""
$checklistFile = "security\adversarial-review-checklist.md"
if (Test-Path $checklistFile) {
    $checklistContent = Get-Content $checklistFile -Raw -Encoding UTF8
    Write-Host "  -> 已加载端点专用审查清单 ($checklistFile)" -ForegroundColor Gray
} else {
    Write-Host "  [WARN] 未找到清单文件，将使用通用审查提示词" -ForegroundColor DarkYellow
}

# ──────────────────────────── 步骤 4: 组装并执行审查 ────────────────────────────
Write-Host ""
Write-Host "[4/5] 执行 PC4 对抗性安全审查..." -ForegroundColor Yellow
Write-Host "  -> 提示: 此过程可能需要几分钟，请耐心等待" -ForegroundColor Gray
Write-Host ""

# 组装审查上下文
$reviewContext = @"
## 审查上下文

- **审查时间**: $timestamp
- **审查对象**: PR/Branch #$PR
- **基准分支**: $baseBranch
- **变更文件数**: $changedFileCount
- **代码变更行数**: $diffLines

## 变更文件列表

````
$changedFiles
````

## 代码变更 (Diff)

````diff
$diffContent
````

---

请对以上代码变更进行完整的对抗性安全审查，按照提示词中指定的格式输出审查报告。
"@

# 加载主提示词
$reviewPrompt = ""
if (Test-Path $promptFile) {
    $reviewPrompt = Get-Content $promptFile -Raw -Encoding UTF8
} else {
    Write-Host "  [FATAL] 未找到审查提示词文件: $promptFile" -ForegroundColor Red
    exit 3
}

# 合并全部内容
$fullPrompt = $reviewPrompt + "`n`n---`n`n" + $checklistContent + "`n`n---`n`n" + $reviewContext

# 调用 Claude Code
try {
    $claudeExists = Get-Command claude -ErrorAction SilentlyContinue
    if (-not $claudeExists) {
        Write-Host "[FATAL] 未找到 claude 命令。请先安装并配置 Claude Code CLI。" -ForegroundColor Red
        # 保存审查上下文以便手动执行
        $promptDumpFile = "${reportDir}\pc4-prompt-${PR}-${timestamp}.txt"
        $fullPrompt | Out-File -FilePath $promptDumpFile -Encoding UTF8
        Write-Host "  -> 审查上下文已保存到 $promptDumpFile" -ForegroundColor Gray
        Write-Host "  -> 手动执行: claude -p `"`$(cat $promptDumpFile)`"" -ForegroundColor Gray
        exit 3
    }

    # 通过管道将内容传给 claude
    $fullPrompt | claude -p --output-format markdown 2>&1 | Out-File -FilePath $reportFile -Encoding UTF8

    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Claude Code 执行异常 (exit code: $LASTEXITCODE)" -ForegroundColor Red
        $promptDumpFile = "${reportDir}\pc4-prompt-${PR}-${timestamp}.txt"
        $fullPrompt | Out-File -FilePath $promptDumpFile -Encoding UTF8
        Write-Host "  -> 审查上下文已保存到 $promptDumpFile 以便手动审查" -ForegroundColor Gray
        exit 2
    }
} catch {
    Write-Host "[ERROR] 执行过程中发生异常: $_" -ForegroundColor Red
    exit 2
}

# ──────────────────────────── 步骤 5: 记录发现 ────────────────────────────
Write-Host ""
Write-Host "[5/5] 更新对抗性发现数据库..." -ForegroundColor Yellow

try {
    # 尝试从报告中提取关键判定信息
    $reportContent = Get-Content $reportFile -Raw -Encoding UTF8 -ErrorAction SilentlyContinue

    $goNogo = "UNKNOWN"
    if ($reportContent -match "APPROVED|REJECTED|CONDITIONAL") {
        $goNogo = $Matches[0]
    }

    $blockingCount = 0
    $nonBlockingCount = 0
    if ($reportContent) {
        $blockingCount = ([regex]::Matches($reportContent, "BLOCKING-\d+")).Count
        $nonBlockingCount = ([regex]::Matches($reportContent, "NON_BLOCKING-\d+")).Count
    }

    # 写入 JSONL 记录
    $findingRecord = @{
        timestamp = $timestamp
        pr = $PR
        platform = "windows"
        report = $reportFile
        go_nogo = $goNogo
        blocking = $blockingCount
        non_blocking = $nonBlockingCount
        diff_size = $diffLines
    } | ConvertTo-Json -Compress

    Add-Content -Path $findingsFile -Value $findingRecord -Encoding UTF8
    Write-Host "  -> 发现记录已写入 $findingsFile" -ForegroundColor Gray
} catch {
    Write-Host "  [WARN] 更新发现记录失败: $_" -ForegroundColor DarkYellow
}

# ──────────────────────────── 完成 ────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  PC4 安全审查完成" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "判定: $goNogo" -ForegroundColor $(if ($goNogo -eq "APPROVED") { "Green" } elseif ($goNogo -eq "REJECTED") { "Red" } else { "Yellow" })
Write-Host "报告: $reportFile" -ForegroundColor White
Write-Host "阻塞性问题: $blockingCount" -ForegroundColor $(if ($blockingCount -gt 0) { "Red" } else { "Green" })
Write-Host "非阻塞性问题: $nonBlockingCount" -ForegroundColor $(if ($nonBlockingCount -gt 0) { "Yellow" } else { "Green" })
Write-Host "发现记录: $findingsFile" -ForegroundColor Gray
Write-Host ""
Write-Host "查看报告: notepad $reportFile" -ForegroundColor Gray
Write-Host "或: code $reportFile" -ForegroundColor Gray
Write-Host "============================================" -ForegroundColor Cyan

# 若有阻塞性问题，返回非零退出码以在 CI/CD 中阻断流水线
if ($blockingCount -gt 0) {
    Write-Host ""
    Write-Host "!! 存在阻塞性安全问题，CI/CD 流水线应阻断 !!" -ForegroundColor Red
    exit 1
}

exit 0
