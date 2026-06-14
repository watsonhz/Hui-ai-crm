/**
 * E2E: 未登录拦截 / Token过期 (TASK-016 Part B)
 */
import { test, expect } from '@playwright/test';

const BASE = 'http://192.168.0.170:3000';

test.describe('认证守卫 — 未登录拦截', () => {

  test('未登录访问 /bidding 应跳转登录页', async ({ page }) => {
    await page.goto(`${BASE}/bidding`);
    await page.waitForTimeout(1000);
    const url = page.url();
    // 应包含 login 或重定向回登录
    expect(url).toMatch(/login|auth|\/\/$/);
  });

  test('未登录访问 /projects 应跳转登录页', async ({ page }) => {
    await page.goto(`${BASE}/projects`);
    await page.waitForTimeout(1000);
    expect(page.url()).toMatch(/login|auth|\/\/$/);
  });

  test('未登录访问 /customers 应跳转登录页', async ({ page }) => {
    await page.goto(`${BASE}/customers`);
    await page.waitForTimeout(1000);
    expect(page.url()).toMatch(/login|auth|\/\/$/);
  });

  test('未登录访问 /acceptance 应跳转登录页', async ({ page }) => {
    await page.goto(`${BASE}/acceptance`);
    await page.waitForTimeout(1000);
    expect(page.url()).toMatch(/login|auth|\/\/$/);
  });

  test('未登录访问 /settings 应跳转登录页', async ({ page }) => {
    await page.goto(`${BASE}/settings`);
    await page.waitForTimeout(1000);
    expect(page.url()).toMatch(/login|auth|\/\/$/);
  });

  test('访问不存在的路由不崩溃', async ({ page }) => {
    await page.goto(`${BASE}/xyz-nonexistent`);
    await page.waitForTimeout(1000);
    await expect(page.locator('body')).toBeVisible();
  });
});
