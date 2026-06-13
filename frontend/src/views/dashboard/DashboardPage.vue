<script setup lang="ts">
import { ref, onMounted } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent, GridComponent,
} from 'echarts/components'

use([CanvasRenderer, BarChart, LineChart, PieChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

// ---- 概览卡片 ----
const stats = ref([
  { label: '今日拜访', value: 28, color: '#409EFF', icon: 'User' },
  { label: '进行中项目', value: 15, color: '#67C23A', icon: 'List' },
  { label: '招标中', value: 8, color: '#E6A23C', icon: 'Document' },
  { label: '本月签约', value: 12, color: '#F56C6C', icon: 'Checked' },
])

// ---- 月度趋势 ----
const trendOption = ref({
  tooltip: { trigger: 'axis' },
  legend: { data: ['拜访次数', '新增客户', '签约数'] },
  grid: { left: '0', right: '10px', bottom: '0', top: '40px', containLabel: true },
  xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
  yAxis: { type: 'value' },
  series: [
    { name: '拜访次数', type: 'bar', data: [120, 132, 101, 134, 156, 182], itemStyle: { color: '#409EFF', borderRadius: [4, 4, 0, 0] } },
    { name: '新增客户', type: 'line', data: [25, 30, 28, 35, 42, 48], smooth: true, itemStyle: { color: '#67C23A' } },
    { name: '签约数', type: 'line', data: [8, 10, 9, 12, 15, 18], smooth: true, itemStyle: { color: '#E6A23C' } },
  ],
})

// ---- 客户行业分布 ----
const pieOption = ref({
  tooltip: { trigger: 'item' },
  legend: { bottom: '0' },
  series: [{
    type: 'pie', radius: ['45%', '75%'], center: ['50%', '45%'],
    label: { show: false },
    data: [
      { value: 35, name: '政府/国企' },
      { value: 28, name: '制造业' },
      { value: 22, name: 'IT/互联网' },
      { value: 18, name: '金融' },
      { value: 15, name: '医疗' },
    ],
  }],
})

// ---- 项目阶段分布 ----
const stageOption = ref({
  tooltip: { trigger: 'axis' },
  grid: { left: '0', right: '10px', bottom: '0', top: '20px', containLabel: true },
  xAxis: { type: 'category', data: ['初步接洽', '需求分析', '方案演示', '报价', '谈判', '签约', '交付', '验收', '维保'] },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar', data: [42, 35, 28, 22, 18, 12, 20, 15, 10],
    itemStyle: { color: '#409EFF', borderRadius: [4, 4, 0, 0] },
  }],
})
</script>

<template>
  <div class="dashboard">
    <!-- 概览卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col v-for="s in stats" :key="s.label" :xs="12" :sm="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div>
              <p class="stat-label">{{ s.label }}</p>
              <p class="stat-value" :style="{ color: s.color }">{{ s.value }}</p>
            </div>
            <div class="stat-icon" :style="{ background: s.color }">
              <el-icon :size="24" color="#fff"><component :is="s.icon" /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区 -->
    <el-row :gutter="16" class="chart-row">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header><span class="card-title">月度运营趋势</span></template>
          <v-chart :option="trendOption" style="height: 340px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header><span class="card-title">客户行业分布</span></template>
          <v-chart :option="pieOption" style="height: 340px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="chart-row">
      <el-col :span="24">
        <el-card shadow="hover">
          <template #header><span class="card-title">项目阶段分布</span></template>
          <v-chart :option="stageOption" style="height: 260px" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.dashboard { .stats-row { margin-bottom: 16px; } }

.stat-card {
  .stat-content {
    display: flex; align-items: center; justify-content: space-between;
    .stat-label { font-size: 13px; color: #909399; margin-bottom: 6px; }
    .stat-value { font-size: 28px; font-weight: 700; }
    .stat-icon {
      width: 48px; height: 48px; border-radius: 12px;
      display: flex; align-items: center; justify-content: center;
    }
  }
}

.chart-row { margin-bottom: 16px; }
.card-title { font-size: 15px; font-weight: 600; }
</style>
