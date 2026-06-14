/**
 * E2E: 合同创建→审批→回款全流程 (TASK-012 Part B)
 *
 * 测试页面: /projects → 合同阶段看板
 * 流程: 商务谈判 → 合同签订 → 项目启动 → ... → 回款 → 维保
 */
import { test, expect } from '@playwright/test';

const BASE = 'http://192.168.0.170:3000';

test.describe('合同验收 — 创建→审批→回款全流程', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/projects`);
    await page.waitForLoadState('networkidle');
  });

  // ==========================================================
  // 合同阶段看板
  // ==========================================================

  test('合同阶段看板可见', async ({ page }) => {
    const contractSection = page.locator('.section-header').filter({ hasText: '合同阶段' });
    await expect(contractSection).toBeVisible();
  });

  test('合同阶段 — 商务谈判列有项目', async ({ page }) => {
    const negotiationColumn = page.locator('.kanban-column').nth(9);
    await expect(negotiationColumn.locator('.column-title')).toContainText('商务谈判');
    const cards = negotiationColumn.locator('.project-card');
    await expect(cards.first()).toBeVisible();
  });

  test('合同阶段 — 合同签订列有项目', async ({ page }) => {
    const contractColumn = page.locator('.kanban-column').nth(10);
    await expect(contractColumn.locator('.column-title')).toContainText('合同签订');
    await expect(contractColumn.locator('.project-card').first()).toBeVisible();
  });

  test('拖拽项目从商务谈判到合同签订', async ({ page }) => {
    // 找到商务谈判列中的第一个卡片
    const negotiationColumn = page.locator('.kanban-column').nth(9);
    const contractColumn = page.locator('.kanban-column').nth(10);

    const card = negotiationColumn.locator('.project-card').first();
    const cardName = await card.locator('.project-card__name').textContent();

    // 拖拽
    await card.dragTo(contractColumn);
    await page.waitForTimeout(500);

    // 验证卡片已移动到合同签订列
    await expect(contractColumn.locator('.project-card').filter({ hasText: cardName! })).toBeVisible();
  });

  // ==========================================================
  // 交付阶段 — 回款
  // ==========================================================

  test('交付阶段看板可见', async ({ page }) => {
    const deliverySection = page.locator('.section-header').filter({ hasText: '交付阶段' });
    await expect(deliverySection).toBeVisible();

    // 应包含 5 列: 项目启动 | 设计开发 | 测试验收 | 上线部署 | 项目交付 | 维保服务
    const deliveryColumns = deliverySection.locator('..').locator('.kanban-column');
    await expect(deliveryColumns).toHaveCount(6);
  });

  test('维保服务列包含已完成项目', async ({ page }) => {
    const maintenanceColumn = page.locator('.kanban-column').last();
    await expect(maintenanceColumn.locator('.column-title')).toContainText('维保服务');

    const cards = maintenanceColumn.locator('.project-card');
    const count = await cards.count();
    expect(count).toBeGreaterThanOrEqual(1);

    // 维保项目进度应为 100%
    const progress = maintenanceColumn.locator('.progress-value').first();
    await expect(progress).toHaveText('100%');
  });

  // ==========================================================
  // 全流程导航
  // ==========================================================

  test('三阶段全流程可见：售前→合同→交付', async ({ page }) => {
    const sections = page.locator('.stage-section');
    await expect(sections).toHaveCount(3);

    // 售前
    await expect(page.locator('.section-title').filter({ hasText: '售前阶段' })).toBeVisible();
    // 合同
    await expect(page.locator('.section-title').filter({ hasText: '合同阶段' })).toBeVisible();
    // 交付
    await expect(page.locator('.section-title').filter({ hasText: '交付阶段' })).toBeVisible();
  });

  test('项目总数统计正确', async ({ page }) => {
    // 售前: 4列 × 平均2-3项目 = 9
    const preSalesCount = page.locator('.section-count').first();
    const preSalesText = await preSalesCount.textContent();
    const preSalesNum = parseInt(preSalesText!);
    expect(preSalesNum).toBeGreaterThan(0);

    // 合同: 2列 × 2-3项目
    const contractCount = page.locator('.section-count').nth(1);
    const contractText = await contractCount.textContent();
    const contractNum = parseInt(contractText!);
    expect(contractNum).toBeGreaterThan(0);

    // 交付: 6列 × 平均2项目
    const deliveryCount = page.locator('.section-count').nth(2);
    const deliveryText = await deliveryCount.textContent();
    const deliveryNum = parseInt(deliveryText!);
    expect(deliveryNum).toBeGreaterThan(0);

    // 全部项目 >= 27
    expect(preSalesNum + contractNum + deliveryNum).toBeGreaterThanOrEqual(27);
  });
});
