<script setup lang="ts">
import { ref, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { GraphChart } from 'echarts/charts'
import { TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, GraphChart, TooltipComponent, LegendComponent])

interface Node { id: string; name: string; category: number; symbolSize: number; role: string; influence: number; dept: string }
interface Link { source: string; target: string; label: string; weight: number }

const categories = [
  { name: '经济决策者' }, { name: '技术决策者' }, { name: '使用者' },
  { name: 'Coach' }, { name: '推荐者' }, { name: '影响者' },
  { name: '守门员' }, { name: '审批者' },
]
const catColors = ['#F56C6C','#409EFF','#67C23A','#E6A23C','#9B59B6','#1ABC9C','#F39C12','#E74C3C']

const nodes: Node[] = [
  { id: '1', name: '张总', category: 0, symbolSize: 60, role: '经济决策者', influence: 9, dept: 'CEO办公室' },
  { id: '2', name: '王工', category: 1, symbolSize: 50, role: '技术决策者', influence: 8, dept: '技术部' },
  { id: '3', name: '赵经理', category: 2, symbolSize: 40, role: '使用者', influence: 5, dept: '业务部' },
  { id: '4', name: '刘主任', category: 3, symbolSize: 30, role: 'Coach', influence: 4, dept: '办公室' },
  { id: '5', name: '陈处长', category: 4, symbolSize: 35, role: '推荐者', influence: 6, dept: '信息化处' },
  { id: '6', name: '李助理', category: 5, symbolSize: 25, role: '影响者', influence: 3, dept: '总经办' },
  { id: '7', name: '周部长', category: 6, symbolSize: 28, role: '守门员', influence: 4, dept: '采购部' },
  { id: '8', name: '孙主任', category: 7, symbolSize: 32, role: '审批者', influence: 5, dept: '财务部' },
]

const links: Link[] = [
  { source: '1', target: '2', label: '直属汇报', weight: 8 },
  { source: '1', target: '4', label: '多年同事', weight: 6 },
  { source: '1', target: '8', label: '审批依赖', weight: 7 },
  { source: '2', target: '3', label: '项目协作', weight: 7 },
  { source: '2', target: '5', label: '技术交流', weight: 5 },
  { source: '3', target: '6', label: '日常工作', weight: 6 },
  { source: '4', target: '6', label: '间接关系', weight: 3 },
  { source: '5', target: '7', label: '采购相关', weight: 4 },
  { source: '7', target: '8', label: '审批流程', weight: 5 },
  { source: '3', target: '7', label: '需求对接', weight: 4 },
]

const viewMode = ref<'point' | 'surface' | 'trend'>('point')
const selectedNode = ref<Node | null>(null)

const graphOption = computed(() => ({
  tooltip: { formatter: (p: any) => p.dataType === 'node' ? `<b>${p.name}</b><br/>${p.data.role} · ${p.data.dept}<br/>影响力: ${p.data.influence}/10` : `${p.data.label}<br/>亲密度: ${p.data.weight}/10` },
  legend: { data: categories.map(c => c.name), bottom: 0 },
  series: [{
    type: 'graph', layout: 'force', roam: true, draggable: true,
    force: { repulsion: viewMode.value === 'point' ? 300 : viewMode.value === 'surface' ? 150 : 500, edgeLength: viewMode.value === 'surface' ? [200, 350] : [100, 200] },
    categories: categories.map((c, i) => ({ name: c.name, itemStyle: { color: catColors[i] } })),
    data: nodes.map(n => ({ ...n, itemStyle: { color: catColors[n.category] }, value: n.influence })),
    links: links.map(l => ({ ...l, lineStyle: { width: l.weight * 0.6, curveness: 0.2 } })),
    label: { show: true, fontSize: 12 }, emphasis: { focus: 'adjacency', lineStyle: { width: 8 } },
  }],
}))

function showDetail(n: any) { selectedNode.value = n.data as Node }
</script>

<template>
  <div class="decision-graph">
    <div class="graph-toolbar">
      <el-radio-group v-model="viewMode" size="small">
        <el-radio-button value="point">点·关键关系</el-radio-button>
        <el-radio-button value="surface">面·普遍关系</el-radio-button>
        <el-radio-button value="trend">势·组织关系</el-radio-button>
      </el-radio-group>
    </div>
    <v-chart :option="graphOption" style="height:500px" autoresize @click="showDetail" />
    <el-dialog v-model="!!selectedNode" :title="selectedNode?.name" width="380px">
      <template v-if="selectedNode">
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="角色">{{ selectedNode.role }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{ selectedNode.dept }}</el-descriptions-item>
          <el-descriptions-item label="影响力">{{ selectedNode.influence }}/10</el-descriptions-item>
        </el-descriptions>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.graph-toolbar { text-align: center; margin-bottom: 12px; }
</style>
