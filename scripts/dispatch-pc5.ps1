Set-Location C:\DevProjects\ai-crm
git checkout -b feature/TASK-004-qa-setup 2>$null
git checkout feature/TASK-004-qa-setup 2>$null
Write-Host "PC5 on branch: $(git branch --show-current)"

$job = Start-Job -ScriptBlock {
    Set-Location C:\DevProjects\ai-crm
    & 'C:\Users\Administrator\AppData\Roaming\npm\claude.cmd' -p 'Please read tasks/todo/TASK-004-qa-framework-setup.md. Set up QA testing framework: 1) pip install pytest pytest-asyncio pytest-cov pytest-xdist httpx locust faker 2) npm install -g @playwright/test and install chromium 3) Create tests/ directory structure 4) Create pytest.ini 5) Document /qa workflow. After each step, git add/commit.'
}
Write-Host "PC5 Job started: $($job.Id)"
