import { test, expect } from '@playwright/test';

test.describe('合同审批流程', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/contracts');
    await page.waitForSelector('.el-table');
  });

  test('合同列表加载', async ({ page }) => {
    await expect(page.locator('text=合同管理')).toBeVisible();
    const rows = page.locator('.el-table__body-wrapper tbody tr');
    await expect(rows.first()).toBeVisible();
  });

  test('点击合同打开详情Dialog', async ({ page }) => {
    await page.locator('.el-table__body-wrapper tbody tr').first().click();
    await expect(page.locator('.el-dialog')).toBeVisible();
    await expect(page.locator('text=审批状态流')).toBeVisible();
  });

  test('合同详情含回款计划', async ({ page }) => {
    await page.locator('.el-table__body-wrapper tbody tr').first().click();
    await expect(page.locator('text=回款计划')).toBeVisible();
  });
});
