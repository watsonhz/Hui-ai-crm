@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0.."

echo ============================================
echo  AI-CRM FINAL QA — 全量回归 + 性能终测
echo ============================================
echo  %date% %time%
echo.

set PYTEST_OPTS=-v --tb=line -o "addopts=-v --tb=line -p no:warnings"

echo [1/4] API Regression (142 tests)...
python -m pytest tests/api/ tests/unit/ tests/security/ %PYTEST_OPTS%
if %errorlevel% neq 0 (
    echo [FAIL] API regression
    exit /b 1
)
echo [PASS] API Regression

echo.
echo [2/4] E2E Regression (61 tests)...
npx playwright test --project=chrome --reporter=html 2>nul
if %errorlevel% neq 0 (
    echo [WARN] Some E2E tests failed
) else (
    echo [PASS] E2E Regression
)

echo.
echo [3/4] Performance Final (100 users, 180s)...
python -m locust -f tests/performance/locustfile-sprint3.py ^
  --host=http://192.168.0.170:8000 ^
  --headless -u 100 -r 10 -t 180s ^
  --html=tests/reports/performance-final.html ^
  --csv=tests/reports/perf-final 2>nul
echo [DONE] Performance report: tests/reports/performance-final.html

echo.
echo [4/4] Docker Validation...
docker-compose config > nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] docker-compose.yml is valid
) else (
    echo [WARN] docker-compose validation failed
)

echo.
echo ============================================
echo  FINAL QA COMPLETE
echo  Reports: tests/reports/
echo ============================================
