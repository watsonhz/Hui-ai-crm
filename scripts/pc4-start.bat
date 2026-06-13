@echo off
cd /d C:\DevProjects\ai-crm
git checkout feature/TASK-003-security-setup 2>nul
start "PC4-SEC" /MIN C:\Users\Administrator\AppData\Roaming\npm\claude.cmd -p "Please read tasks/todo/TASK-003-security-audit-setup.md. Install security tools: pip install bandit safety. Run bandit scan on backend/. Run npm audit on frontend/. Document the /cso workflow. After each step git add/commit. When done, create tasks/done/TASK-003-done.md and echo DONE > C:\temp-task003-done.txt"
echo PC4 Started
