@echo off
chcp 65001 >nul
echo ============================================
echo  Sprint2 Performance Baseline
echo  AI-CRM v4.0 — TASK-008 Part C
echo ============================================
echo.

cd /d "%~dp0.."

echo Running Locust baseline (100 users, 120s)...
echo Output: tests/reports/performance-baseline-sprint2.html
echo.

python -m locust -f tests/performance/locustfile.py ^
  --host=http://192.168.0.170:8000 ^
  --headless ^
  -u 100 ^
  -r 10 ^
  -t 120s ^
  --html=tests/reports/performance-baseline-sprint2.html ^
  --csv=tests/reports/perf-sprint2

echo.
echo ============================================
echo  Baseline complete!
echo  Report: tests/reports/performance-baseline-sprint2.html
echo ============================================
