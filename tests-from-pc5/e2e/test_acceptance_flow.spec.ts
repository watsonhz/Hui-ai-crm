/**
 * E2E: 分阶段验收流程测试 (TASK-012 Part B)
 *
 * 测试页面: /acceptance — 验收管理
 * 流程: 待验收 → 验收中 → 已通过 → 已驳回 → 回款确认
 */
import { test, expect } from '@playwright/test';

const BASE = 'http://192.168.0.170:3000';

test.describe('验收管理 — 分阶段验收流程', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/acceptance`);
    await page.waitForLoadState('networkidle');
  });

  // ==========================================================
  // 页面结构
  // ==========================================================

  test('页面加载：显示验收管理标题', async ({ page }) => {
    await expect(page.locator('.page-header h2')).toHaveText('验收管理');
  });

  test('Tab 切换：待验收/已通过/已驳回/回款', async ({ page }) => {
    const tabs = page.locator('.acceptance-tabs .el-tab-pane');
    // 通过 label 检查 tab 存在
    await expect(page.locator('.el-tabs__item').filter({ hasText: '待验收' })).toBeVisible();
    await expect(page.locator('.el-tabs__item').filter({ hasText: '已通过' })).toBeVisible();
    await expect(page.locator('.el-tabs__item').filter({ hasText: '已驳回' })).toBeVisible();
    await expect(page.locator('.el-tabs__item').filter({ hasText: '回款确认' })).toBeVisible();
  });

  // ==========================================================
  // 待验收
  // ==========================================================

  test('待验收 tab — 表格有数据', async ({ page }) => {
    const table = page.locator('.el-table').first();
    await expect(table).toBeVisible();
    // 表头
    await expect(table.locator('th').filter({ hasText: '项目名称' })).toBeVisible();
    await expect(table.locator('th').filter({ hasText: '客户' })).toBeVisible();
    await expect(table.locator('th').filter({ hasText: '验收日期' })).toBeVisible();
    await expect(table.locator('th').filter({ hasText: '验收标准' })).toBeVisible();
  });

  test('待验收 — 操作按钮：发起验收 / 驳回', async ({ page }) => {
    const actionButtons = page.locator('.el-table__body .el-button').first();
    await expect(actionButtons).toBeVisible();
    // 应该有「发起验收」按钮
    await expect(page.locator('.el-button--primary').filter({ hasText: '发起验收' }).first()).toBeVisible();
    // 应该有「驳回」按钮
    await expect(page.locator('.el-button--danger').filter({ hasText: '驳回' }).first()).toBeVisible();
  });

  test('待验收 — 验收标准标签可见', async ({ page }) => {
    const criteriaTags = page.locator('.criteria-tag').first();
    await expect(criteriaTags).toBeVisible();
  });

  // ==========================================================
  // Tab 切换
  // ==========================================================

  test('切换到已通过 tab', async ({ page }) => {
    await page.locator('.el-tabs__item').filter({ hasText: '已通过' }).click();
    await page.waitForTimeout(300);
    await expect(page.locator('.el-tabs__item.is-active').filter({ hasText: '已通过' })).toBeVisible();
  });

  test('切换到已驳回 tab', async ({ page }) => {
    await page.locator('.el-tabs__item').filter({ hasText: '已驳回' }).click();
    await page.waitForTimeout(300);
    await expect(page.locator('.el-tabs__item.is-active').filter({ hasText: '已驳回' })).toBeVisible();
  });

  test('切换到回款确认 tab', async ({ page }) => {
    await page.locator('.el-tabs__item').filter({ hasText: '回款确认' }).click();
    await page.waitForTimeout(300);
    await expect(page.locator('.el-tabs__item.is-active').filter({ hasText: '回款确认' })).toBeVisible();
  });

  test('分阶段验收完整流程导航', async ({ page }) => {
    // 1. 待验收 → 查看数据
    await expect(page.locator('.el-table__body')).toBeVisible();

    // 2. 切换到已通过
    await page.locator('.el-tabs__item').filter({ hasText: '已通过' }).click();
    await page.waitForTimeout(300);

    // 3. 切换到已驳回
    await page.locator('.el-tabs__item').filter({ hasText: '已驳回' }).click();
    await page.waitForTimeout(300);

    // 4. 切换到回款确认
    await page.locator('.el-tabs__item').filter({ hasText: '回款确认' }).click();
    await page.waitForTimeout(300);

    // 所有 tab 都不应该崩溃
    await expect(page.locator('body')).toBeVisible();
  });
});
