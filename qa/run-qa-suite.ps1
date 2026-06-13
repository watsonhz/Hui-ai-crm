<#
.SYNOPSIS
PC5 完整QA测试套件 (v3.1.0 第二闸)
#>
param([switch]$SkipPerf, [switch]$SkipE2E)

$ErrorActionPreference = "Continue"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$reportDir = "$PSScriptRoot\report-html"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PC5 QA 测试套件启动 — $timestamp" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Step 1: Newman API 测试
Write-Host "`n[1/4] Newman API 测试..." -ForegroundColor Yellow
newman run "$PSScriptRoot/newman/crm-api-collection.json" `
  --env-var base_url=http://localhost:8000 `
  -r htmlextra --reporter-htmlextra-export "$reportDir/api-report.html" `
  --color 2>&1
if ($LASTEXITCODE -ne 0) { Write-Host "⚠️ Newman 有失败用例" -ForegroundColor Red }
else { Write-Host "✅ Newman 全部通过" -ForegroundColor Green }

# Step 2: Playwright E2E 测试
if (-not $SkipE2E) {
  Write-Host "`n[2/4] Playwright E2E 测试..." -ForegroundColor Yellow
  npx playwright test --config="$PSScriptRoot/playwright.config.ts" 2>&1
  if ($LASTEXITCODE -ne 0) { Write-Host "⚠️ Playwright 有失败用例" -ForegroundColor Red }
  else { Write-Host "✅ Playwright 全部通过" -ForegroundColor Green }
}

# Step 3: k6 性能测试
if (-not $SkipPerf) {
  Write-Host "`n[3/4] k6 性能测试..." -ForegroundColor Yellow
  k6 run "$PSScriptRoot/k6/customer-api-load.js" --summary-export="$reportDir/perf-summary.json" 2>&1
  if ($LASTEXITCODE -ne 0) { Write-Host "⚠️ 性能阈值未达标" -ForegroundColor Red }
  else { Write-Host "✅ 性能测试通过" -ForegroundColor Green }
}

# Step 4: 生成QA报告
Write-Host "`n[4/4] 生成QA报告..." -ForegroundColor Yellow
$reportPath = "$reportDir/qa-report-$($timestamp -replace '[: ]', '-').html"
Write-Host "报告位置: $reportPath" -ForegroundColor White
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  PC5 QA 测试套件完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
