@echo off
cd /d C:\DevProjects\ai-crm
git checkout feature/TASK-004-qa-setup 2>nul
start "PC5-QA" /MIN C:\Users\Administrator\AppData\Roaming\npm\claude.cmd -p "Please read tasks/todo/TASK-004-qa-framework-setup.md. Install: pip install pytest pytest-asyncio pytest-cov httpx locust faker. Install npm Playwright with chromium. Create tests/ structure. Create pytest.ini. Document the /qa workflow. After each step git add/commit. When done, create tasks/done/TASK-004-done.md and echo DONE > C:\temp-task004-done.txt"
echo PC5 Started
