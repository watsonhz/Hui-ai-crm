/**
 * E2E: 招投标全流程测试 (TASK-008 Part A)
 *
 * 测试页面: /bidding — 招投标管理看板
 * 9 列状态: 线索 | 商机确认 | 方案设计 | 投标中 | 商务谈判 | 中标 | 丢标 | 项目交付 | 维保
 */
import { test, expect } from '@playwright/test';

const BASE = 'http://192.168.0.170:3000';

test.describe('招投标管理 — 看板全流程', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/bidding`);
    await page.waitForLoadState('networkidle');
  });

  // ==========================================================
  // 页面结构
  // ==========================================================

  test('页面加载：显示标题和新建按钮', async ({ page }) => {
    await expect(page.locator('.page-header h2')).toHaveText('招投标管理');
    const newBtn = page.locator('.page-header .el-button--primary');
    await expect(newBtn).toBeVisible();
    await expect(newBtn).toContainText('新建投标');
  });

  test('看板加载：9 列状态全部显示', async ({ page }) => {
    const columns = page.locator('.kanban-column');
    await expect(columns).toHaveCount(9);

    const expectedLabels = [
      '线索', '商机确认', '方案设计', '投标中',
      '商务谈判', '中标', '丢标', '项目交付', '维保',
    ];
    for (const label of expectedLabels) {
      await expect(page.locator('.column-title').filter({ hasText: label })).toBeVisible();
    }
  });

  test('每列显示正确的项目数量徽章', async ({ page }) => {
    // 验证每列的 badge 数量
    const badges = page.locator('.column-badge .el-badge__content');
    // "线索" 列应有 3 个项目
    await expect(badges.first()).toHaveText('3');
    // "商机确认" 列
    await expect(badges.nth(1)).toHaveText('2');
    // "方案设计" 列
    await expect(badges.nth(2)).toHaveText('3');
    // "投标中" 列
    await expect(badges.nth(3)).toHaveText('2');
  });

  test('列中显示空状态', async ({ page }) => {
    // "丢标" 列有项目，不应该为空
    const lostColumn = page.locator('.kanban-column').nth(6);
    await expect(lostColumn.locator('.bid-card')).toHaveCount(2);

    // 点击空列的 class — 所有有项目的列不应出现 column-empty
    const emptySlots = page.locator('.column-empty');
    // 全 9 列都有 mock 数据，空状态不应出现
    await expect(emptySlots).toHaveCount(0);
  });

  // ==========================================================
  // 投标卡片
  // ==========================================================

  test('投标卡片显示完整信息', async ({ page }) => {
    const firstCard = page.locator('.bid-card').first();
    // 项目名称
    await expect(firstCard.locator('.bid-card__name')).toHaveText('智慧城市数据中心');
    // 客户
    await expect(firstCard.locator('.bid-card__customer')).toContainText('XX市政府');
    // 金额
    await expect(firstCard.locator('.bid-card__amount')).toContainText('¥580万');
    // 截止日期
    await expect(firstCard.locator('.bid-card__footer')).toContainText('2026-08-15');
  });

  test('紧急投标卡片有红色标签', async ({ page }) => {
    // "智慧城市数据中心" 是紧急（danger）
    const dangerTag = page.locator('.bid-card').first().locator('.el-tag--danger');
    await expect(dangerTag).toBeVisible();
    await expect(dangerTag).toHaveText('紧急');
  });

  test('投标卡片 hover 显示拖拽手柄', async ({ page }) => {
    const card = page.locator('.bid-card').first();
    const handle = card.locator('.bid-card__drag-handle');
    // 默认隐藏
    await expect(handle).toHaveCSS('opacity', '0');
    // hover 后显示
    await card.hover();
    await expect(handle).toHaveCSS('opacity', '1');
  });

  test('投标卡片支持拖拽', async ({ page }) => {
    const sourceCard = page.locator('.bid-card').first();
    const targetColumn = page.locator('.kanban-column').nth(3); // 投标中

    const cardText = await sourceCard.locator('.bid-card__name').textContent();

    // 执行拖拽
    await sourceCard.dragTo(targetColumn);
    await page.waitForTimeout(500);

    // 卡片应出现在目标列
    await expect(targetColumn.locator('.bid-card').filter({ hasText: cardText! })).toBeVisible();
  });

  // ==========================================================
  // 统计数据
  // ==========================================================

  test('总投标数量验证', async ({ page }) => {
    const cards = page.locator('.bid-card');
    await expect(cards).toHaveCount(21);
  });

  test('中标列包含中标项目', async ({ page }) => {
    const wonColumn = page.locator('.kanban-column').nth(5);
    await expect(wonColumn.locator('.bid-card__name').first()).toHaveText('政务OA系统');
    await expect(wonColumn.locator('.bid-card')).toHaveCount(2);
  });
});
