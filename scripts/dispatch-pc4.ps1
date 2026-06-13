Set-Location C:\DevProjects\ai-crm
git checkout -b feature/TASK-003-security-setup 2>$null
git checkout feature/TASK-003-security-setup 2>$null
Write-Host "PC4 on branch: $(git branch --show-current)"

$job = Start-Job -ScriptBlock {
    Set-Location C:\DevProjects\ai-crm
    & 'C:\Users\Administrator\AppData\Roaming\npm\claude.cmd' -p 'Please read tasks/todo/TASK-003-security-audit-setup.md. Set up security audit environment: 1) pip install bandit safety 2) Run bandit scan on backend/ 3) Run npm audit on frontend/ 4) Create security/audit-reports template 5) Document /cso workflow. After each step, git add/commit.'
}
Write-Host "PC4 Job started: $($job.Id)"
