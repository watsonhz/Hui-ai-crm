<script setup lang="ts">
import { ref } from 'vue'
import LTCDashboard from '@/components/visit/LTCDashboard.vue'

const ltcStages = [
  { name: '线索', count: 42, color: '#909399', stuck: 0 },
  { name: '商机确认', count: 28, color: '#409EFF', stuck: 2 },
  { name: '方案设计', count: 15, color: '#67C23A', stuck: 1 },
  { name: '投标报价', count: 10, color: '#E6A23C', stuck: 3 },
  { name: '商务谈判', count: 8, color: '#F56C6C', stuck: 0 },
  { name: '合同签订', count: 6, color: '#9B59B6', stuck: 0 },
  { name: '项目交付', count: 5, color: '#1ABC9C', stuck: 1 },
  { name: '验收回款', count: 3, color: '#E74C3C', stuck: 0 },
  { name: '维保服务', count: 12, color: '#3498DB', stuck: 0 },
]

const selectedProject = ref<any>(null)
const dialogVisible = ref(false)
function openDialog(p: any) { selectedProject.value = p; dialogVisible.value = true }

const projects = [
  { id: 1, name: '中科曙光IT运维平台', customer: '中科曙光', stage: '商务谈判', amount: 5800000, stuck: true, stuckReason: '价格谈判僵持，客户要求再降5%', timeline: ['2025-11 线索', '2025-12 商机确认', '2026-02 方案演示', '2026-04 投标', '2026-06 商务谈判中'] },
  { id: 2, name: '张江智慧园区', customer: '上海张江集团', stage: '方案设计', amount: 12600000, stuck: false, stuckReason: '', timeline: ['2026-03 线索', '2026-04 商机确认', '2026-06 方案设计中'] },
  { id: 3, name: '浙江大数据平台', customer: '浙江省大数据局', stage: '维保服务', amount: 8600000, stuck: false, stuckReason: '', timeline: ['2024-03 线索', '2024-06 中标', '2024-12 交付', '2025-06 验收', '2026-01 维保'] },
  { id: 4, name: '华为云扩容', customer: '深圳华为', stage: '投标报价', amount: 3200000, stuck: true, stuckReason: '竞品低价竞争，我方报价高15%', timeline: ['2026-01 线索', '2026-03 商机', '2026-05 投标报价中'] },
]
</script>

<template>
  <div class="ltc-page">
    <h2 class="page-title">LTC 全链路看板</h2>

    <!-- 概览看板 -->
    <LTCDashboard :stages="ltcStages" />

    <!-- 项目列表 + 时间线 -->
    <h3 class="section-title">项目详情</h3>
    <el-row :gutter="16">
      <el-col v-for="p in projects" :key="p.id" :span="6" style="margin-bottom:16px">
        <el-card shadow="hover" class="project-card" @click="openDialog(p)">
          <div class="card-top">
            <span class="project-name">{{ p.name }}</span>
            <el-tag v-if="p.stuck" type="danger" size="small">⚠️ 卡顿</el-tag>
          </div>
          <div class="card-meta">
            <span>{{ p.customer }}</span>
            <span>¥ {{ p.amount.toLocaleString() }}</span>
          </div>
          <el-tag type="primary" size="small">{{ p.stage }}</el-tag>
        </el-card>
      </el-col>
    </el-row>

    <!-- 项目时间线 Dialog -->
    <el-dialog v-model="dialogVisible" :title="selectedProject?.name" width="600px">
      <template v-if="selectedProject">
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="客户">{{ selectedProject.customer }}</el-descriptions-item>
          <el-descriptions-item label="金额">¥ {{ selectedProject.amount.toLocaleString() }}</el-descriptions-item>
          <el-descriptions-item label="当前阶段">{{ selectedProject.stage }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag v-if="selectedProject.stuck" type="danger">卡顿 — {{ selectedProject.stuckReason }}</el-tag>
            <el-tag v-else type="success">正常推进</el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <h4 style="margin:20px 0 12px">📅 全生命周期时间线</h4>
        <el-timeline>
          <el-timeline-item
            v-for="(t, i) in selectedProject.timeline" :key="t"
            :timestamp="t" placement="top"
            :color="i === selectedProject.timeline.length - 1 ? '#409EFF' : '#67C23A'"
          >
            {{ t.split(' ')[1] || t }}
          </el-timeline-item>
        </el-timeline>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.page-title { margin-bottom: 20px; }
.section-title { margin: 24px 0 12px; font-size: 17px; font-weight: 600; }
.project-card { cursor: pointer; transition: transform 0.2s; &:hover { transform: translateY(-2px); } }
.card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.project-name { font-size: 14px; font-weight: 600; }
.card-meta { display: flex; justify-content: space-between; font-size: 12px; color: #909399; margin-bottom: 8px; }
</style>
