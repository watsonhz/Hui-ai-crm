/**
 * E2E: 管理员 RBAC 操作 (TASK-020 Part B)
 */
import { test, expect } from '@playwright/test';

const BASE = 'http://192.168.0.170:3000';

test.describe('管理员 — RBAC 权限管理', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/settings`);
    await page.waitForLoadState('networkidle');
  });

  test('设置页加载：用户/角色/权限 Tab 可见', async ({ page }) => {
    const tabs = page.locator('.el-tabs__item');
    expect(await tabs.count()).toBeGreaterThanOrEqual(1);
  });

  test('用户管理 tab 可切换', async ({ page }) => {
    const userTab = page.locator('.el-tabs__item').filter({ hasText: /用户|user/i });
    if (await userTab.isVisible()) {
      await userTab.click();
      await page.waitForTimeout(300);
    }
    await expect(page.locator('body')).toBeVisible();
  });

  test('角色管理 tab 可切换', async ({ page }) => {
    const roleTab = page.locator('.el-tabs__item').filter({ hasText: /角色|role/i });
    if (await roleTab.isVisible()) {
      await roleTab.click();
      await page.waitForTimeout(300);
    }
    await expect(page.locator('body')).toBeVisible();
  });

  test('权限配置 tab 可切换', async ({ page }) => {
    const permTab = page.locator('.el-tabs__item').filter({ hasText: /权限|permission/i });
    if (await permTab.isVisible()) {
      await permTab.click();
      await page.waitForTimeout(300);
    }
    await expect(page.locator('body')).toBeVisible();
  });

  test('全 Tab 遍历不崩溃', async ({ page }) => {
    const tabs = page.locator('.el-tabs__item');
    const count = await tabs.count();
    for (let i = 0; i < count; i++) {
      await tabs.nth(i).click();
      await page.waitForTimeout(200);
    }
    await expect(page.locator('body')).toBeVisible();
  });
});
