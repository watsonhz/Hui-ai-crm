@echo off
cd /d C:\DevProjects\ai-crm
git checkout -b feature/TASK-004-qa-testing 2>nul
git checkout feature/TASK-004-qa-testing 2>nul
start "PC5-QA" /MIN C:\Users\Administrator\AppData\Roaming\npm\claude.cmd -p "You are PC5 QA Engineer. Read backend/app/api/v1/bidding.py, projects.py, organizations.py and write pytest tests for ALL endpoints. Each test: valid case, invalid input, edge case, auth test. Write to tests/api/test_bidding.py, tests/api/test_projects.py, tests/api/test_organizations.py. Use httpx or pytest+FastAPI TestClient. After each file, git add/commit. When done echo DONE>C:\\temp-pc5-done.txt"
echo PC5 QA started
