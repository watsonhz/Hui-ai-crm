import { test, expect } from '@playwright/test';

test.describe('客户管理 CRUD E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/customers');
  });

  test('客户列表页面正常加载', async ({ page }) => {
    await expect(page.locator('.el-table')).toBeVisible();
    await expect(page.getByText('客户列表')).toBeVisible();
  });

  test('搜索功能正常', async ({ page }) => {
    await page.fill('input[placeholder*="客户名称"]', '张');
    await page.click('button:has-text("搜索")');
    await page.waitForResponse((res) => res.url().includes('/api/v1/customers/') && res.status() === 200);
  });

  test('分页功能正常', async ({ page }) => {
    await expect(page.locator('.el-pagination')).toBeVisible();
  });

  test('新增客户对话框', async ({ page }) => {
    await page.click('button:has-text("新增客户")');
    await expect(page.locator('.el-dialog')).toBeVisible();
  });
});
