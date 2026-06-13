import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  retries: 1,
  use: { baseURL: 'http://localhost:5173', screenshot: 'on', video: 'retain-on-failure' },
  projects: [
    { name: 'chrome-win11', use: { ...devices['Desktop Chrome'] } },
    { name: 'edge-win11', use: { ...devices['Desktop Edge'] } },
    { name: 'safari-mac', use: { ...devices['Desktop Safari'] } },
    { name: 'firefox-win', use: { ...devices['Desktop Firefox'] } },
    { name: 'chrome-mobile', use: { ...devices['Pixel 5'] } },
  ],
  reporter: [['html', { outputFolder: 'report-html' }], ['json', { outputFile: 'report.json' }]],
});
