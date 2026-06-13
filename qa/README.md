# PC5 QA 测试框架 (v3.1.0 第二闸)

PC5 — QA 测试工程师专机。Windows Server 2019 @ 192.168.0.253。

## 目录结构

```
qa/
├── e2e/                  # Playwright E2E 测试
├── k6/                   # 性能/负载测试
├── newman/               # API 测试集合
├── report-html/          # 测试报告输出
├── playwright.config.ts  # Playwright 5浏览器配置
├── run-qa-suite.ps1      # 完整QA套件脚本
├── package.json          # 依赖管理
└── README.md
```

## 快速开始

```powershell
# 1. 安装依赖
cd C:\DevProjects\ai-crm\qa
npm install

# 2. 安装 Playwright 浏览器
npx playwright install --with-deps

# 3. 运行完整QA套件
powershell -File run-qa-suite.ps1

# 或分步运行
npm run qa:api    # Newman API 测试
npm run qa:e2e    # Playwright E2E
npm run qa:perf   # k6 性能测试
```

## 定时回归

```powershell
# 注册 Windows 计划任务（每日 3:00 AM）
powershell -File register-scheduled-task.ps1
```

## 报告位置

- API 报告: `qa/report-html/api-report.html`
- E2E 报告: `qa/report-html/index.html`
- IIS 发布: `http://192.168.0.253:8080/qa-reports/`
