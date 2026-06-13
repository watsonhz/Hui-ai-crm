@echo off
chcp 65001 >nul
echo ============================================
echo  Sprint3 Performance Baseline
echo  AI + PGVector + CRUD 综合压测
echo ============================================
echo.

cd /d "%~dp0.."

echo Target: AI P95 ^< 3s ^| CRUD P95 ^< 500ms ^| PGVector P95 ^< 200ms
echo Running 50 users for 180s...
echo.

python -m locust -f tests/performance/locustfile-sprint3.py ^
  --host=http://192.168.0.170:8000 ^
  --headless ^
  -u 50 ^
  -r 5 ^
  -t 180s ^
  --html=tests/reports/performance-sprint3.html ^
  --csv=tests/reports/perf-sprint3

echo.
echo ============================================
echo  Report: tests/reports/performance-sprint3.html
echo ============================================
