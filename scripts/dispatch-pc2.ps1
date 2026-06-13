Set-Location C:\DevProjects\ai-crm
git checkout -b feature/TASK-002-frontend-layout 2>$null
git checkout feature/TASK-002-frontend-layout 2>$null
Write-Host "PC2 on branch: $(git branch --show-current)"

$job = Start-Job -ScriptBlock {
    Set-Location C:\DevProjects\ai-crm
    & 'C:\Users\gzzhh\AppData\Roaming\npm\claude.cmd' -p 'Please read tasks/todo/TASK-002-crm-frontend-layout.md and build the Vue3 CRM management console. Create: 1) MainLayout with collapsible sidebar + breadcrumbs 2) Vue Router with all 11 routes 3) The 5-visit flow (PrepareCard, QuickRecord, AISummary) 3-page component. Use Element Plus + TypeScript + ECharts. After each component, git add/commit with descriptive messages.'
}
Write-Host "PC2 Job started: $($job.Id)"
