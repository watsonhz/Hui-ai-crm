import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright 端到端测试配置 — AI-CRM 前端。
 *
 * 运行方式:
 *   npx playwright test
 *   npx playwright test --ui     (可视化模式)
 *   npx playwright test --headed (有头浏览器)
 */
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { outputFolder: 'tests/reports/playwright-report' }],
    ['json', { outputFile: 'tests/reports/playwright-results.json' }],
  ],
  use: {
    baseURL: 'http://192.168.0.170:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chrome',
      use: {
        ...devices['Desktop Chrome'],
        channel: 'chrome',  // 使用系统已安装的 Chrome，无需下载 Chromium
      },
    },
  ],
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
});
