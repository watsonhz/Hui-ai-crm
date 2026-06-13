@echo off
cd /d C:\DevProjects\ai-crm
git checkout feature/TASK-002-frontend-layout 2>nul
start "PC2-CRM" /MIN C:\Users\gzzhh\AppData\Roaming\npm\claude.cmd -p "Please read tasks/todo/TASK-002-crm-frontend-layout.md and build the Vue3 CRM admin. Create MainLayout with collapsible sidebar and breadcrumbs, Vue Router with all 11 routes, and the 5-visit 3-screen flow components (VisitPrepare, VisitRecord, VisitSummary). Use Element Plus, TypeScript, ECharts. After each major file create, git add/commit. When done, create tasks/done/TASK-002-done.md and echo DONE > C:\temp-task002-done.txt"
echo PC2 Started
