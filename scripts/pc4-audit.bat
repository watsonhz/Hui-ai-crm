@echo off
cd /d C:\DevProjects\ai-crm
git checkout -b feature/TASK-003-security-audit 2>nul
git checkout feature/TASK-003-security-audit 2>nul
start "PC4-AUDIT" /MIN C:\Users\Administrator\AppData\Roaming\npm\claude.cmd -p "You are PC4, the independent security auditor. Your job is to adversarially audit PC3's backend code. Read ALL of the following files and find security issues: backend/app/api/v1/bidding.py, backend/app/api/v1/projects.py, backend/app/api/v1/organizations.py, backend/app/models/bidding.py, backend/app/models/project.py, backend/app/models/organization.py, backend/app/schemas/*.py. Check for: SQL injection, XSS, auth bypass, missing input validation, insecure state transitions, hardcoded secrets, CORS issues. For each finding: severity(Critical/High/Medium/Low), OWASP category, file+line, attack scenario, fix. Output findings to security/audit-reports/audit-TASK-001.md. When done, git add/commit/push and echo DONE>C:\temp-pc4-done.txt"
echo PC4 Audit started
