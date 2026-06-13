import { test, expect } from '@playwright/test';

test.describe('5次拜访三屏流程', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/relationships');
    await page.waitForSelector('.visit-steps');
  });

  test('屏1-准备卡：显示拜访信息', async ({ page }) => {
    await expect(page.locator('text=中科曙光')).toBeVisible();
    await expect(page.locator('text=拜访信息')).toBeVisible();
    await expect(page.locator('.alert-item').first()).toBeVisible();
  });

  test('屏2-快速记录：语音模式', async ({ page }) => {
    await page.click('text=快速记录');
    await page.waitForSelector('.voice-btn-area');
    await expect(page.locator('text=语音记录')).toBeVisible();
    await page.click('.voice-btn-area button');
    await page.waitForTimeout(3500);
    await expect(page.locator('.voice-textarea')).toBeVisible();
  });

  test('屏3-AI纪要：行动项列表', async ({ page }) => {
    await page.click('text=AI 纪要');
    await page.waitForSelector('.minutes-editor');
    await expect(page.locator('text=AI 生成纪要')).toBeVisible();
    await expect(page.locator('.action-card').first()).toBeVisible();
  });
});
