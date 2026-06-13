<script setup lang="ts">
import { ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, FunnelChart, GaugeChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent, CalendarComponent } from 'echarts/components'

use([CanvasRenderer, BarChart, LineChart, PieChart, FunnelChart, GaugeChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, VisualMapComponent, CalendarComponent])

// ---- 概览卡片 ----
const stats = ref([
  { label: '今日拜访', value: 28, color: '#409EFF', icon: 'User' },
  { label: '进行中项目', value: 15, color: '#67C23A', icon: 'List' },
  { label: '招标中', value: 8, color: '#E6A23C', icon: 'Document' },
  { label: '本月签约', value: 12, color: '#F56C6C', icon: 'Checked' },
])

// ---- 1. 销售漏斗图 ----
const funnelOption = ref({
  tooltip: { trigger: 'item', formatter: '{b}: {c} 个 ({d}%)' },
  series: [{
    type: 'funnel', left: '10%', width: '80%', sort: 'descending', gap: 2,
    label: { show: true, position: 'inside', fontSize: 13 },
    itemStyle: { borderColor: '#fff', borderWidth: 1 },
    data: [
      { value: 180, name: '线索' },
      { value: 120, name: '商机确认' },
      { value: 56, name: '方案演示' },
      { value: 32, name: '投标报价' },
      { value: 18, name: '商务谈判' },
      { value: 12, name: '中标' },
    ],
  }],
})

// ---- 2. 业绩趋势图 (line) ----
const lineOption = ref({
  tooltip: { trigger: 'axis' },
  legend: { data: ['合同额', '回款额', '目标'] },
  grid: { left: '0', right: '10px', bottom: '0', top: '40px', containLabel: true },
  xAxis: { type: 'category', data: ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'] },
  yAxis: { type: 'value', axisLabel: { formatter: (v: number) => (v / 10000).toFixed(0) + '万' } },
  series: [
    { name: '合同额', type: 'line', data: [280,320,250,410,380,520,480,560,430,610,550,680], smooth: true, areaStyle: { opacity: 0.1 }, itemStyle: { color: '#409EFF' } },
    { name: '回款额', type: 'line', data: [200,280,230,350,320,450,410,490,380,520,470,590], smooth: true, areaStyle: { opacity: 0.05 }, itemStyle: { color: '#67C23A' } },
    { name: '目标', type: 'line', data: [350,350,350,400,400,450,450,500,500,550,550,600], lineStyle: { type: 'dashed' }, itemStyle: { color: '#F56C6C' } },
  ],
})

// ---- 3. 客户分布图 (双饼图：行业 + 等级) ----
const pieOption = ref({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0 },
  series: [
    {
      name: '行业分布', type: 'pie', radius: ['30%', '50%'], center: ['25%', '45%'],
      label: { formatter: '{b}\n{d}%', fontSize: 11 },
      data: [
        { value: 35, name: '政府/国企' }, { value: 28, name: '制造业' },
        { value: 22, name: 'IT/互联网' }, { value: 18, name: '金融' }, { value: 15, name: '医疗' },
      ],
    },
    {
      name: '客户等级', type: 'pie', radius: ['30%', '50%'], center: ['75%', '45%'],
      label: { formatter: '{b}\n{d}%', fontSize: 11 },
      data: [
        { value: 15, name: 'A级', itemStyle: { color: '#F56C6C' } },
        { value: 32, name: 'B级', itemStyle: { color: '#E6A23C' } },
        { value: 48, name: 'C级', itemStyle: { color: '#409EFF' } },
        { value: 25, name: 'D级', itemStyle: { color: '#67C23A' } },
      ],
    },
  ],
})

// ---- 4. 项目看板概览 (gauge + bar) ----
const gaugeOption = ref({
  series: [
    { type: 'gauge', center: ['20%', '55%'], radius: '70%', startAngle: 200, endAngle: -20, min: 0, max: 90,
      data: [{ value: 72, name: '项目健康度' }],
      detail: { formatter: '{value}%', fontSize: 16, offsetCenter: [0, '60%'] },
      axisLine: { lineStyle: { width: 12, color: [[0.5,'#F56C6C'],[0.75,'#E6A23C'],[1,'#67C23A']] } },
    },
    { type: 'gauge', center: ['55%', '55%'], radius: '70%', startAngle: 200, endAngle: -20, min: 0, max: 30,
      data: [{ value: 5, name: '卡顿项目' }],
      detail: { formatter: '{value} 个', fontSize: 16, offsetCenter: [0, '60%'] },
      axisLine: { lineStyle: { width: 12, color: [[0.3,'#67C23A'],[0.6,'#E6A23C'],[1,'#F56C6C']] } },
    },
    { type: 'gauge', center: ['85%', '55%'], radius: '60%', startAngle: 200, endAngle: -20, min: 0, max: 60,
      data: [{ value: 8, name: '逾期预警' }],
      detail: { formatter: '{value} 天', fontSize: 16, offsetCenter: [0, '60%'] },
      axisLine: { lineStyle: { width: 10, color: [[0.2,'#67C23A'],[0.5,'#E6A23C'],[1,'#F56C6C']] } },
    },
  ],
})

// ---- 5. AI诊断信号汇总 (heatmap) ----
const hours = ['0-2时','2-4时','4-6时','6-8时','8-10时','10-12时','12-14时','14-16时','16-18时','18-20时','20-22时','22-24时']
const days = ['流失风险','合同到期','商机降温','付款逾期','决策链缺口','竞品活跃','满意度下降','服务异常']
const heatData: [number, number, number][] = []
for (let i = 0; i < days.length; i++) {
  for (let j = 0; j < hours.length; j++) {
    heatData.push([j, i, Math.round(Math.random() * 100)])
  }
}
const heatmapOption = ref({
  tooltip: { formatter: (p: any) => `${days[p.value[1]]} / ${hours[p.value[0]]}: ${p.value[2]} 条信号` },
  grid: { left: '110px', right: '20px', top: '10px', bottom: '30px' },
  xAxis: { type: 'category', data: hours, axisLabel: { fontSize: 10 } },
  yAxis: { type: 'category', data: days, axisLabel: { fontSize: 11 } },
  visualMap: { min: 0, max: 100, calculable: true, orient: 'horizontal', left: 'center', bottom: 0,
    inRange: { color: ['#f0f9ff', '#bae6fd', '#7dd3fc', '#38bdf8', '#0ea5e9', '#0369a1'] },
  },
  series: [{ type: 'heatmap', data: heatData, label: { show: false } }],
})
</script>

<template>
  <div class="dashboard">
    <!-- 概览卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col v-for="s in stats" :key="s.label" :xs="12" :md="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div><p class="stat-label">{{ s.label }}</p><p class="stat-value" :style="{ color: s.color }">{{ s.value }}</p></div>
            <div class="stat-icon" :style="{ background: s.color }"><el-icon :size="24" color="#fff"><component :is="s.icon" /></el-icon></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 漏斗 + 业绩趋势 -->
    <el-row :gutter="16" class="chart-row">
      <el-col :span="8">
        <el-card shadow="hover"><template #header><span class="card-title">销售漏斗</span></template>
          <v-chart :option="funnelOption" style="height:340px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="hover"><template #header><span class="card-title">业绩趋势（万元）</span></template>
          <v-chart :option="lineOption" style="height:340px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- 客户分布 + 项目看板 -->
    <el-row :gutter="16" class="chart-row">
      <el-col :span="12">
        <el-card shadow="hover"><template #header><span class="card-title">客户分布（行业 / 等级）</span></template>
          <v-chart :option="pieOption" style="height:320px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover"><template #header><span class="card-title">项目看板概览</span></template>
          <v-chart :option="gaugeOption" style="height:320px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <!-- AI 诊断热力图 -->
    <el-row :gutter="16" class="chart-row">
      <el-col :span="24">
        <el-card shadow="hover"><template #header><span class="card-title">AI 诊断信号汇总（24h热力图）</span></template>
          <v-chart :option="heatmapOption" style="height:340px" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped lang="scss">
.dashboard { .stats-row { margin-bottom: 16px; } }
.stat-card {
  .stat-content { display: flex; align-items: center; justify-content: space-between; }
  .stat-label { font-size: 13px; color: #909399; margin-bottom: 6px; }
  .stat-value { font-size: 28px; font-weight: 700; }
  .stat-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
}
.chart-row { margin-bottom: 16px; }
.card-title { font-size: 15px; font-weight: 600; }
</style>
