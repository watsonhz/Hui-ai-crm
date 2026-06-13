param(
    [string]$TaskFile = ""
)

if ($TaskFile -eq "") {
    Write-Host "用法: .\dispatch-tasks.ps1 -TaskFile TASK-001"
    exit
}

$assignee = (Get-Content "tasks/todo/$TaskFile.md" | Select-String "assignee:").ToString().Split(":")[1].Trim()

# v3.1.0 IP mapping per Section 2.3
switch ($assignee) {
    "pc2" { $target = "192.168.0.169"; $path = "D:/DevProjects/ai-crm" }
    "pc3" { $target = "192.168.0.170"; $path = "~/DevProjects/ai-crm" }
    "pc4" { $target = "192.168.0.171"; $path = "D:/DevProjects/ai-crm" }
    "pc5" { $target = "192.168.0.253"; $path = "D:/DevProjects/ai-crm" }
    default { Write-Host "未知分配目标: $assignee"; exit 1 }
}

Write-Host "🚀 分发 $TaskFile → $assignee ($target)"
ssh $target "cd $path && git pull && cat tasks/todo/$TaskFile.md | claude -p '按任务文件完成开发并提交'"
Write-Host "✅ 任务已下发"
