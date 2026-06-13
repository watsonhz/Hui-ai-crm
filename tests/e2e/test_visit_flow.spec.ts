/**
 * E2E: 5 次拜访三屏流程测试 (TASK-008 Part A)
 *
 * 测试页面: /relationships — 关系维护 → 拜访流程
 * 三屏: 准备卡 → 快速记录 → AI 纪要
 */
import { test, expect } from '@playwright/test';

const BASE = 'http://192.168.0.170:3000';

test.describe('关系维护 — 5次拜访三屏流程', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto(`${BASE}/relationships`);
    await page.waitForLoadState('networkidle');
  });

  // ==========================================================
  // 屏1：准备卡
  // ==========================================================

  test('屏1-准备卡：显示拜访信息', async ({ page }) => {
    // 默认应显示屏1
    await expect(page.locator('.screen-content').first()).toBeVisible();
    // 拜访信息卡片
    await expect(page.locator('.info-card')).toBeVisible();
    await expect(page.locator('.info-card')).toContainText('中科曙光');
    await expect(page.locator('.info-card')).toContainText('张总（CIO）');
    await expect(page.locator('.info-card')).toContainText('2026-06-15');
  });

  test('屏1-准备卡：显示告警信息', async ({ page }) => {
    const alerts = page.locator('.alert-item');
    await expect(alerts).toHaveCount(3);
    // 第一条告警应为 warning 类型（合同付款条款）
    await expect(alerts.first()).toContainText('合同付款条款');
    // 第二条为 info（采购预算）
    await expect(alerts.nth(1)).toContainText('采购预算');
    // 第三条为 danger（竞争对手）
    await expect(alerts.nth(2)).toContainText('华为云');
  });

  test('屏1-准备卡：待办事项列表', async ({ page }) => {
    const todoItems = page.locator('.todo-item');
    await expect(todoItems).toHaveCount(4);
    // 第2项标记为已完成（发邮件确认议程）
    const secondCheckbox = todoItems.nth(1).locator('.el-checkbox');
    await expect(secondCheckbox).toHaveClass(/is-checked/);
  });

  test('屏1-准备卡：建议议题显示', async ({ page }) => {
    const topics = page.locator('.topic-list li');
    await expect(topics).toHaveCount(4);
    await expect(topics.first()).toContainText('年度运维平台升级方案汇报');
    await expect(topics.nth(2)).toContainText('AI运维');
  });

  test('屏1-准备卡：展开历史拜访记录', async ({ page }) => {
    const collapseHeader = page.locator('.detail-collapse .el-collapse-item__header');
    await collapseHeader.click();
    // 等待时间线展开
    await page.waitForTimeout(400);
    const timeline = page.locator('.el-timeline');
    await expect(timeline).toBeVisible();
    const timelineItems = timeline.locator('.el-timeline-item');
    await expect(timelineItems).toHaveCount(3);
  });

  // ==========================================================
  // 屏2：快速记录
  // ==========================================================

  test('屏2-快速记录：切换到屏2', async ({ page }) => {
    // 点击「快速记录」radio button
    await page.locator('.el-radio-button').filter({ hasText: '快速记录' }).click();
    await page.waitForTimeout(300);
    // 应显示录音/Ctrl 切换按钮
    await expect(page.locator('.record-tabs')).toBeVisible();
  });

  test('屏2-快速记录：语音模式录音', async ({ page }) => {
    await page.locator('.el-radio-button').filter({ hasText: '快速记录' }).click();
    // 默认应在语音模式
    await expect(page.locator('.voice-area')).toBeVisible();
    // 录音按钮
    const micButton = page.locator('.voice-area .el-button');
    await expect(micButton).toBeVisible();
    // 点击开始录音
    await micButton.click();
    await page.waitForTimeout(500);
    // 应显示"录音中..."
    await expect(page.locator('.voice-hint')).toContainText('录音中');
    // 等待模拟录音完成 (3s)
    await page.waitForTimeout(3500);
    // 应显示语音转文字结果
    await expect(page.locator('.voice-area textarea')).toBeVisible();
    await expect(page.locator('.voice-area textarea')).toContainText('中科曙光');
  });

  test('屏2-快速记录：手动勾选模式', async ({ page }) => {
    await page.locator('.el-radio-button').filter({ hasText: '快速记录' }).click();
    // 切换到手动勾选
    await page.locator('.el-radio-button').filter({ hasText: '手动勾选' }).click();
    await page.waitForTimeout(300);
    // 8 个勾选项
    const checkboxes = page.locator('.manual-area .el-checkbox');
    await expect(checkboxes).toHaveCount(8);
    // 勾选第1项
    await checkboxes.first().click();
    await expect(checkboxes.first()).toHaveClass(/is-checked/);
  });

  // ==========================================================
  // 屏3：AI 纪要
  // ==========================================================

  test('屏3-AI纪要：切换到屏3', async ({ page }) => {
    await page.locator('.el-radio-button').filter({ hasText: 'AI 纪要' }).click();
    await page.waitForTimeout(300);
    // 应显示纪要内容
    const minutesCard = page.locator('.minutes-row');
    await expect(minutesCard).toBeVisible();
    // 左栏 - AI 生成纪要
    await expect(page.locator('.minutes-row textarea').first()).toContainText('拜访纪要');
  });

  test('屏3-AI纪要：纪要包含关键信息', async ({ page }) => {
    await page.locator('.el-radio-button').filter({ hasText: 'AI 纪要' }).click();
    await page.waitForTimeout(300);

    const minutesText = await page.locator('.minutes-row textarea').first().inputValue();
    expect(minutesText).toContain('中科曙光');
    expect(minutesText).toContain('张总');
    expect(minutesText).toContain('AI运维');
    expect(minutesText).toContain('## 一、会议背景');
    expect(minutesText).toContain('## 二、核心内容');
    expect(minutesText).toContain('## 三、关键决策');
  });

  test('屏3-AI纪要：行动项列表', async ({ page }) => {
    await page.locator('.el-radio-button').filter({ hasText: 'AI 纪要' }).click();
    await page.waitForTimeout(300);

    const actionItems = page.locator('.action-item');
    await expect(actionItems).toHaveCount(5);
    // P0 项应有 danger 标签
    const p0Tags = actionItems.locator('.el-tag--danger');
    await expect(p0Tags).toHaveCount(2);
  });

  test('屏3-AI纪要：三屏完整导航', async ({ page }) => {
    // 1 → 2 → 3 顺序导航
    const steps = page.locator('.el-steps .el-step');
    await expect(steps).toHaveCount(3);

    // 到屏2
    await page.locator('.el-radio-button').filter({ hasText: '快速记录' }).click();
    await expect(page.locator('.el-steps .el-step.is-success').first()).toBeVisible();

    // 到屏3
    await page.locator('.el-radio-button').filter({ hasText: 'AI 纪要' }).click();
    // 屏1和屏2应标记为完成
    await expect(page.locator('.el-steps .el-step.is-success')).toHaveCount(2);
  });
});
