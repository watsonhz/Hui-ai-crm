<script setup lang="ts">
import { computed } from 'vue'
import { useVisitStore } from '@/stores/visit'

const emit = defineEmits<{ next: [] }>()
const store = useVisitStore()

const stageColors: Record<string, string> = {
  '第1次': '#409EFF', '第2次': '#67C23A', '第3次': '#E6A23C',
  '第4次': '#F56C6C', '第5次': '#9B59B6',
}

function toggleTopicEdit(id: number) {
  const t = store.topics.find(t => t.id === id)
  if (t) t.editable = !t.editable
}
</script>

<template>
  <div class="prepare-screen">
    <!-- 顶部：阶段标签 + 客户 -->
    <div class="prepare-header">
      <el-tag :color="stageColors[store.visitInfo.stage]" effect="dark" size="large">
        {{ store.visitInfo.stage }}
      </el-tag>
      <h2 class="customer-name">{{ store.visitInfo.customerName }}</h2>
    </div>

    <!-- 告警区 -->
    <div v-if="store.alerts.length" class="alerts-section">
      <el-alert
        v-for="(a, i) in store.alerts" :key="i"
        :title="a.text" :type="a.type" :closable="false" show-icon
        class="alert-item"
      />
    </div>

    <!-- 核心信息 5 行 -->
    <el-card shadow="hover" class="info-card">
      <template #header><span class="card-title">拜访信息</span></template>
      <el-descriptions :column="2" border size="default">
        <el-descriptions-item label="拜访时间">{{ store.visitInfo.visitTime }}</el-descriptions-item>
        <el-descriptions-item label="地点">{{ store.visitInfo.location }}</el-descriptions-item>
        <el-descriptions-item label="我方参会人" :span="2">{{ store.visitInfo.ourAttendees }}</el-descriptions-item>
        <el-descriptions-item label="客户方参会人" :span="2">{{ store.visitInfo.customerAttendees }}</el-descriptions-item>
        <el-descriptions-item label="拜访目标" :span="2">{{ store.visitInfo.purpose }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 上次待办 -->
    <el-card v-if="store.unfinishedActions.length" shadow="hover" class="actions-card">
      <template #header>
        <span class="card-title">待办事项</span>
        <el-badge :value="store.unfinishedActions.length" type="warning" class="badge" />
      </template>
      <div v-for="item in store.unfinishedActions" :key="item.id" class="action-row">
        <el-tag :type="item.priority === 'P0' ? 'danger' : item.priority === 'P1' ? 'warning' : 'info'" size="small">
          {{ item.priority }}
        </el-tag>
        <span class="action-text">{{ item.content }}</span>
        <span class="action-due">{{ item.assignee }} · {{ item.due }}</span>
      </div>
    </el-card>

    <!-- 建议议题（可编辑） -->
    <el-card shadow="hover" class="topics-card">
      <template #header><span class="card-title">建议议题</span></template>
      <div v-for="t in store.topics" :key="t.id" class="topic-row">
        <el-icon color="#409EFF" :size="16"><ChatDotRound /></el-icon>
        <span v-if="!t.editable" class="topic-text" @dblclick="toggleTopicEdit(t.id)">{{ t.text }}</span>
        <el-input v-else v-model="t.text" size="small" @blur="toggleTopicEdit(t.id)" />
        <el-button size="small" text @click="toggleTopicEdit(t.id)">
          <el-icon><Edit /></el-icon>
        </el-button>
      </div>
    </el-card>

    <!-- 可展开详情 -->
    <el-collapse class="detail-collapse">
      <el-collapse-item title="完整客户背景 / 决策链 / 历史拜访" name="detail">
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="联系人">{{ store.visitInfo.contacts }}</el-descriptions-item>
          <el-descriptions-item label="客户背景">该客户为2025年中标后转化的长期合作客户，目前在谈二期扩容项目。</el-descriptions-item>
          <el-descriptions-item label="上次拜访">2026-05-20 — 方案演示，客户对AI运维模块表示浓厚兴趣。</el-descriptions-item>
        </el-descriptions>
      </el-collapse-item>
    </el-collapse>

    <!-- 底部按钮 -->
    <div class="bottom-bar">
      <el-button type="primary" size="large" @click="emit('next')">
        开始拜访 <el-icon><ArrowRight /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.prepare-screen { max-width: 900px; margin: 0 auto; }
.prepare-header { display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }
.customer-name { font-size: 20px; font-weight: 700; margin: 0; }
.alerts-section .alert-item { margin-bottom: 8px; }
.info-card, .actions-card, .topics-card { margin-bottom: 16px; }
.card-title { font-size: 15px; font-weight: 600; }
.badge { margin-left: 8px; }
.action-row { display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
.action-text { flex: 1; font-size: 14px; }
.action-due { font-size: 12px; color: #909399; white-space: nowrap; }
.topic-row { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid #f5f5f5; }
.topic-text { flex: 1; font-size: 14px; cursor: pointer; &:hover { color: #409EFF; } }
.detail-collapse { margin-bottom: 20px; }
.bottom-bar { text-align: center; padding: 20px 0; }
</style>
