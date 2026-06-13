<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

type ReportType = 'daily' | 'weekly' | 'monthly'

const activeTab = ref<ReportType>('daily')
const selectedDate = ref<Date>(new Date())
const generating = ref(false)
const reportReady = ref(false)

// ---- 日报数据 ----
const dailyReport = ref({
  completedTasks: [
    { id: 1, text: '完成中科曙光IT运维平台方案演示', done: true },
    { id: 2, text: '与华为云渠道经理沟通合作意向', done: true },
    { id: 3, text: '整理本周客户拜访纪要并同步团队', done: true },
    { id: 4, text: '审核并提交三份投标技术方案', done: true },
    { id: 5, text: '参加产品部门AI功能迭代评审会', done: false },
  ],
  keyProgress: [
    { text: '中科曙光项目进入商务谈判阶段，客户确认项目优先级并同意提前1个月启动', tag: '重大进展' },
    { text: '本月签约目标已完成80%（12/15），预计下周可提前达成', tag: '进度领先' },
    { text: 'AI运维模块POC演示获得3家客户正面反馈，转化率有望提升', tag: '产品突破' },
  ],
  pendingIssues: [
    { text: '中科曙光合同付款条款待法务确认，已超5个工作日', tag: '需跟进' },
    { text: '上海电气项目技术方案需补充安全合规说明，截止本周五', tag: '紧急' },
    { text: '团队成员李工请假至下周一，客户拜访排期需重新调整', tag: '排期风险' },
  ],
  nextPlan: [
    '明日赴上海电气进行现场技术交流，确认安全合规需求细节',
    '完成中科曙光正式报价函（含3%优惠方案）并发送张总',
    '与法务部门沟通合同付款条款模板化方案，减少审批周期',
    '组织团队周会，同步各项目进展并调整下周拜访计划',
  ],
})

// ---- 周报数据 ----
const weeklyReport = ref({
  completedTasks: [
    { id: 1, text: '完成中科曙光、上海电气、中芯国际三家重点客户拜访', done: true },
    { id: 2, text: 'AI运维平台v3.2方案通过内部评审并发布', done: true },
    { id: 3, text: '参与华东区行业峰会，获取23条有效商机线索', done: true },
    { id: 4, text: '团队完成季度销售技能培训（参加率100%）', done: true },
    { id: 5, text: '整理并归档全部客户拜访纪要至知识库', done: true },
  ],
  keyProgress: [
    { text: '本周签约3单，合计金额680万，超额完成周度目标（500万）', tag: '超额完成' },
    { text: '中科曙光项目从需求分析推进至商务谈判阶段，进度较计划提前2周', tag: '进度领先' },
    { text: '新客户拓展：通过行业峰会新增5家潜在客户进入初步接洽阶段', tag: '管道增长' },
  ],
  pendingIssues: [
    { text: '上海电气安全合规说明文档内部审核周期过长，需建立绿色通道机制', tag: '流程优化' },
    { text: '竞争对手华为云在中芯国际项目中报价低于我方15%，需制定应对策略', tag: '竞争压力' },
    { text: '部分历史合同模板未更新新税法条款，需与法务协同修订', tag: '合规风险' },
  ],
  nextPlan: [
    '推进中科曙光POC驻场安排，确保2周内完成技术验证',
    '针对华为云竞争制定差异化方案（侧重AI能力和本地化服务优势）',
    '完成合同模板税法条款更新并同步全团队使用',
    '下周一召开月度经营分析会，复盘Q2业绩并规划Q3策略',
    '安排上海电气安全合规专项沟通会，邀请法务和安服团队参加',
  ],
})

// ---- 月报数据 ----
const monthlyReport = ref({
  completedTasks: [
    { id: 1, text: '月度签约目标15单，实际完成17单（达成率113%）', done: true },
    { id: 2, text: '重点客户拜访覆盖率95%（20/21家），深度交流占比60%', done: true },
    { id: 3, text: 'AI运维产品线月度营收环比增长28%，成为第二大收入来源', done: true },
    { id: 4, text: '团队人员稳定，核心成员留存率100%', done: true },
    { id: 5, text: '客户满意度调查得分4.6/5.0，较上月提升0.2分', done: true },
    { id: 6, text: '知识库月度贡献：新增文档32篇，更新15篇', done: true },
  ],
  keyProgress: [
    { text: '月度营收2,860万，同比增长35%，环比增长12%', tag: '里程碑' },
    { text: 'AI运维产品线成功打入3家行业头部客户，标杆效应初显', tag: '战略突破' },
    { text: '销售团队人均产出较去年同期提升18%，运营效率持续优化', tag: '效率提升' },
  ],
  pendingIssues: [
    { text: '部分大型项目交付周期偏长（平均45天），影响客户满意度评分', tag: '持续关注' },
    { text: '中部地区市场覆盖率不足（仅12%），需制定区域拓展计划', tag: '战略缺口' },
    { text: '合同审批平均周期7.3天，较目标（5天）仍有差距', tag: '效率瓶颈' },
  ],
  nextPlan: [
    '制定Q3季度销售目标（营收3,500万，签约20单）及分解方案',
    '启动中部区域市场拓展：在武汉设立办事处，组建3人先锋团队',
    '优化合同审批流程：推行分级授权机制，目标将平均周期压缩至5天内',
    '加大AI运维产品线投入：Q3计划新增2个行业解决方案模板',
    '组织半年度客户答谢活动，深化重点客户关系',
  ],
})

// ---- 日期选择器配置 ----
const datePickerType = computed(() => {
  const map: Record<ReportType, 'date' | 'week' | 'month'> = {
    daily: 'date',
    weekly: 'week',
    monthly: 'month',
  }
  return map[activeTab.value]
})

const datePlaceholder = computed(() => {
  const map: Record<ReportType, string> = {
    daily: '选择日期',
    weekly: '选择周',
    monthly: '选择月',
  }
  return map[activeTab.value]
})

const dateFormat = computed(() => {
  const map: Record<ReportType, string> = {
    daily: 'YYYY-MM-DD',
    weekly: 'YYYY 第 ww 周',
    monthly: 'YYYY-MM',
  }
  return map[activeTab.value]
})

const currentReport = computed(() => {
  const map: Record<ReportType, typeof dailyReport.value> = {
    daily: dailyReport.value,
    weekly: weeklyReport.value,
    monthly: monthlyReport.value,
  }
  return map[activeTab.value]
})

const reportTitle = computed(() => {
  const map: Record<ReportType, string> = {
    daily: '今日',
    weekly: '本周',
    monthly: '本月',
  }
  return map[activeTab.value]
})

// ---- 操作 ----
function handleGenerate() {
  generating.value = true
  setTimeout(() => {
    generating.value = false
    reportReady.value = true
    ElMessage.success('报告生成成功')
  }, 2000)
}

function handleExportPDF() {
  ElMessage.info('正在导出 PDF...')
}

function handleExportWord() {
  ElMessage.info('正在导出 Word...')
}

function handleSendFeishu() {
  ElMessage.info('正在发送飞书消息...')
}

function handleTabChange() {
  reportReady.value = false
}
</script>

<template>
  <div class="ai-reports-page">
    <!-- 顶部操作栏 -->
    <div class="report-header">
      <div class="header-left">
        <el-date-picker
          v-model="selectedDate"
          :type="datePickerType"
          :placeholder="datePlaceholder"
          :format="dateFormat"
          value-format="YYYY-MM-DD"
          size="default"
          style="width: 220px"
        />
        <el-button
          type="primary"
          :loading="generating"
          :icon="generating ? '' : 'MagicStick'"
          @click="handleGenerate"
        >
          {{ generating ? '生成中...' : '生成报告' }}
        </el-button>
      </div>
      <div class="header-right">
        <el-button @click="handleExportPDF" :disabled="!reportReady">
          <el-icon><Document /></el-icon>导出PDF
        </el-button>
        <el-button @click="handleExportWord" :disabled="!reportReady">
          <el-icon><Document /></el-icon>导出Word
        </el-button>
        <el-button @click="handleSendFeishu" :disabled="!reportReady">
          <el-icon><Promotion /></el-icon>发送飞书
        </el-button>
      </div>
    </div>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab" @tab-change="handleTabChange" class="report-tabs">
      <el-tab-pane label="日报" name="daily" />
      <el-tab-pane label="周报" name="weekly" />
      <el-tab-pane label="月报" name="monthly" />
    </el-tabs>

    <!-- 报告预览区 -->
    <div class="report-body" v-if="reportReady">
      <div class="report-preview">
        <!-- 一、工作完成情况 -->
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <el-icon color="#67C23A"><CircleCheck /></el-icon>
              <span>{{ reportTitle }}工作完成情况</span>
              <el-tag size="small" type="success">
                {{ currentReport.completedTasks.filter((t) => t.done).length }}/{{
                  currentReport.completedTasks.length
                }}
              </el-tag>
            </div>
          </template>
          <div
            v-for="task in currentReport.completedTasks"
            :key="task.id"
            class="checklist-item"
          >
            <el-icon :color="task.done ? '#67C23A' : '#C0C4CC'" :size="18">
              <CircleCheck v-if="task.done" />
              <CircleClose v-else />
            </el-icon>
            <span :class="{ 'text-done': task.done, 'text-pending': !task.done }">
              {{ task.text }}
            </span>
          </div>
        </el-card>

        <!-- 二、关键进展 -->
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <el-icon color="#409EFF"><TrendCharts /></el-icon>
              <span>关键进展</span>
            </div>
          </template>
          <ul class="bullet-list">
            <li v-for="(item, i) in currentReport.keyProgress" :key="i">
              <el-tag size="small" type="success" effect="plain">{{ item.tag }}</el-tag>
              <span>{{ item.text }}</span>
            </li>
          </ul>
        </el-card>

        <!-- 三、待解决问题 -->
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <el-icon color="#E6A23C"><WarningFilled /></el-icon>
              <span>待解决问题</span>
            </div>
          </template>
          <ul class="bullet-list">
            <li v-for="(item, i) in currentReport.pendingIssues" :key="i">
              <el-tag size="small" type="warning" effect="plain">{{ item.tag }}</el-tag>
              <span>{{ item.text }}</span>
            </li>
          </ul>
        </el-card>

        <!-- 四、下一步计划 -->
        <el-card shadow="hover" class="section-card">
          <template #header>
            <div class="section-header">
              <el-icon color="#F56C6C"><List /></el-icon>
              <span>下一步计划</span>
            </div>
          </template>
          <ol class="numbered-list">
            <li v-for="(item, i) in currentReport.nextPlan" :key="i">{{ item }}</li>
          </ol>
        </el-card>
      </div>
    </div>

    <!-- 空状态 -->
    <div class="report-empty" v-else>
      <el-empty description="请选择日期并点击「生成报告」查看工作总结" :image-size="160" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.ai-reports-page {
  max-width: 1000px;
  margin: 0 auto;
}

.report-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.report-tabs {
  margin-bottom: 20px;
}

.report-body {
  animation: fadeIn 0.4s ease;
}

.report-preview {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-card {
  .section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
  }
}

.checklist-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #f5f5f5;

  &:last-child {
    border-bottom: none;
  }

  .text-done {
    color: #303133;
    font-size: 14px;
  }

  .text-pending {
    color: #909399;
    font-size: 14px;
  }
}

.bullet-list {
  list-style: none;
  padding: 0;
  margin: 0;

  li {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 10px 0;
    border-bottom: 1px solid #f5f5f5;
    font-size: 14px;
    line-height: 1.6;

    &:last-child {
      border-bottom: none;
    }
  }
}

.numbered-list {
  padding-left: 20px;
  margin: 0;

  li {
    padding: 10px 0;
    border-bottom: 1px solid #f5f5f5;
    font-size: 14px;
    line-height: 1.6;

    &:last-child {
      border-bottom: none;
    }
  }
}

.report-empty {
  padding: 80px 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
