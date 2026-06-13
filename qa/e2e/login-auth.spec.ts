import { test, expect } from '@playwright/test';

test.describe('登录认证', () => {
  test('未登录访问/dashboard跳转/login', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForURL('**/login**');
    expect(page.url()).toContain('/login');
  });

  test('密码登录成功跳转dashboard', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[placeholder*="用户名"]', 'admin');
    await page.fill('input[placeholder*="密码"]', 'password');
    await page.click('button:has-text("登 录")');
    await page.waitForTimeout(1000);
    expect(page.url()).toContain('/dashboard');
  });

  test('短信登录Tab切换', async ({ page }) => {
    await page.goto('/login');
    await page.click('text=短信登录');
    await expect(page.locator('input[placeholder*="手机号"]')).toBeVisible();
    await expect(page.locator('text=获取验证码')).toBeVisible();
  });

  test('微信登录模式可切换', async ({ page }) => {
    await page.goto('/login');
    await page.click('text=微信登录');
    await expect(page.locator('text=微信扫码登录')).toBeVisible();
  });
});
