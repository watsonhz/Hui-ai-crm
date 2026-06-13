@echo off
chcp 65001 >nul
echo ============================================
echo  TASK-004: QA 测试框架依赖安装
echo  AI-CRM v4.0
echo  执行时间: %date% %time%
echo ============================================
echo.

cd /d "%~dp0..\.."

echo [1/4] 安装 Python 测试依赖...
python -m pip install -r backend\requirements-test.txt
if %errorlevel% neq 0 (
    echo [FAIL] Python 测试依赖安装失败
    exit /b 1
)
echo [OK] Python 测试依赖安装完成
echo.

echo [2/4] 验证 pytest...
python -m pytest --version
if %errorlevel% neq 0 (
    echo [FAIL] pytest 验证失败
    exit /b 1
)
echo [OK] pytest 可用
echo.

echo [3/4] 安装 Playwright...
call npm install -g @playwright/test
if %errorlevel% neq 0 (
    echo [FAIL] Playwright 安装失败
    exit /b 1
)
echo [OK] Playwright 安装完成
echo.

echo [4/4] 安装 Playwright 浏览器...
call npx playwright install chromium
if %errorlevel% neq 0 (
    echo [FAIL] Chromium 浏览器安装失败
    exit /b 1
)
echo [OK] Chromium 浏览器安装完成
echo.

echo ============================================
echo  全部安装完成！运行验证:
echo    pytest tests/unit/test_health.py -v
echo    npx playwright test --browser=chromium
echo ============================================
