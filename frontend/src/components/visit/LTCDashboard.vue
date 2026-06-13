<script setup lang="ts">
import { computed } from 'vue'

interface LtcStage { name: string; count: number; color: string; stuck: number }
const props = defineProps<{ stages: LtcStage[] }>()

const totalProjects = computed(() => props.stages.reduce((s, x) => s + x.count, 0))
const totalStuck = computed(() => props.stages.reduce((s, x) => s + x.stuck, 0))
</script>

<template>
  <div class="ltc-dashboard">
    <!-- 概览 -->
    <el-row :gutter="16" class="overview-row">
      <el-col :span="8">
        <el-statistic title="项目总数" :value="totalProjects" />
      </el-col>
      <el-col :span="8">
        <el-statistic title="卡顿预警" :value="totalStuck">
          <template #suffix>
            <el-tag v-if="totalStuck > 0" type="danger" size="small">{{ totalStuck }} 个</el-tag>
          </template>
        </el-statistic>
      </el-col>
      <el-col :span="8">
        <el-statistic title="转化率" :value="totalProjects > 0 ? Math.round((stages[stages.length-1]?.count || 0) / totalProjects * 100) : 0">
          <template #suffix><span>%</span></template>
        </el-statistic>
      </el-col>
    </el-row>

    <!-- 阶段流 -->
    <div class="pipeline">
      <div v-for="(s, i) in stages" :key="s.name" class="pipeline-stage">
        <div class="stage-card" :style="{ borderTopColor: s.color }">
          <div class="stage-name">{{ s.name }}</div>
          <div class="stage-count" :style="{ color: s.color }">{{ s.count }}</div>
          <div v-if="s.stuck > 0" class="stage-stuck">
            <el-tag type="danger" size="small">⚠️ {{ s.stuck }} 卡顿</el-tag>
          </div>
        </div>
        <div v-if="i < stages.length - 1" class="stage-arrow">→</div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.overview-row { margin-bottom: 24px; }
.pipeline { display: flex; align-items: flex-start; overflow-x: auto; gap: 0; padding: 16px 0; }
.pipeline-stage { display: flex; align-items: center; flex-shrink: 0; }
.stage-card {
  width: 130px; padding: 16px 12px; text-align: center;
  background: #fff; border-radius: 8px; border: 1px solid #e8e8e8; border-top: 3px solid;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.stage-name { font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #333; }
.stage-count { font-size: 24px; font-weight: 700; }
.stage-stuck { margin-top: 6px; }
.stage-arrow { margin: 0 8px; font-size: 20px; color: #c0c4cc; margin-top: 30px; flex-shrink: 0; }
</style>
