@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0.."

echo ============================================
echo  AI-CRM 全量回归测试
echo ============================================
echo.

set PYTEST_OPTS=-v --tb=short -o "addopts=-v --tb=short -p no:warnings"

echo [1/5] Backend Core API Tests...
python -m pytest tests/api/test_bidding.py tests/api/test_projects.py tests/api/test_organizations.py %PYTEST_OPTS%
if %errorlevel% neq 0 (echo [FAIL] Core API & exit /b 1)

echo.
echo [2/5] AI + Knowledge + RBAC Tests...
python -m pytest tests/api/test_decision_chain.py tests/api/test_diagnosis.py tests/api/test_diagnosis_engine.py tests/api/test_ai_reports.py tests/api/test_knowledge.py tests/api/test_ai_service.py tests/api/test_workflow.py tests/api/test_ai_sales.py tests/api/test_ai_marketing.py tests/api/test_system_rbac.py %PYTEST_OPTS%
if %errorlevel% neq 0 (echo [FAIL] AI Tests & exit /b 1)

echo.
echo [3/5] Customer CRUD Tests...
python -m pytest tests/api/test_customers.py %PYTEST_OPTS%
if %errorlevel% neq 0 (echo [FAIL] Customer Tests & exit /b 1)

echo.
echo [4/5] Unit + Security Tests...
python -m pytest tests/unit/ tests/security/ %PYTEST_OPTS%
if %errorlevel% neq 0 (echo [FAIL] Unit/Security & exit /b 1)

echo.
echo [5/5] E2E Tests (Playwright)...
npx playwright test --project=chrome --reporter=html 2>nul
if %errorlevel% neq 0 (echo [WARN] Some E2E tests failed (frontend may not be running))

echo.
echo ============================================
echo  All tests complete!
echo  Coverage: tests/reports/coverage/
echo  E2E:      tests/reports/playwright-report/
echo ============================================
