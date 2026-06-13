<script setup lang="ts">
import { ref } from 'vue'
import { useVisitStore } from '@/stores/visit'
import type { CustomerAttitude, RelationTrend } from '@/types/visit'

const emit = defineEmits<{ next: []; prev: [] }>()
const store = useVisitStore()

const recordingTimer = ref<ReturnType<typeof setInterval> | null>(null)

function toggleVoice() {
  if (store.voiceStatus === 'idle') {
    store.voiceStatus = 'recording'
    recordingTimer.value = setTimeout(() => {
      store.voiceStatus = 'done'
      store.voiceText = '今天拜访整体顺利。客户对我方方案表示认可，特别对AI运维能力模块表现出强烈兴趣。商务方面，客户希望价格再优惠5%，我方初步沟通后认为可在3%范围内让步。客户同意将项目启动时间提前1个月。下一步需安排技术团队驻场做POC演示。关系温度明显升温，客户表态积极。'
    }, 3000)
  } else {
    store.voiceStatus = 'idle'
    store.voiceText = ''
    if (recordingTimer.value) clearTimeout(recordingTimer.value)
  }
}

const attitudes: { label: string; value: CustomerAttitude; color: string }[] = [
  { label: '积极', value: '积极', color: '#67C23A' },
  { label: '观望', value: '观望', color: '#E6A23C' },
  { label: '抵触', value: '抵触', color: '#F56C6C' },
]

const trends: { label: string; value: RelationTrend; icon: string }[] = [
  { label: '升温', value: '升温', icon: 'Top' },
  { label: '稳定', value: '稳定', icon: 'Right' },
  { label: '降温', value: '降温', icon: 'Bottom' },
]
</script>

<template>
  <div class="record-screen">
    <!-- Tab 切换 -->
    <div class="mode-tabs">
      <el-radio-group v-model="store.recordMode" size="large">
        <el-radio-button value="voice">🎤 语音记录</el-radio-button>
        <el-radio-button value="manual">📋 手动勾选</el-radio-button>
      </el-radio-group>
    </div>

    <!-- 语音模式 -->
    <div v-if="store.recordMode === 'voice'" class="voice-section">
      <div class="voice-btn-area">
        <el-button
          :type="store.voiceStatus === 'recording' ? 'danger' : 'primary'"
          size="large" circle @click="toggleVoice"
        >
          <el-icon :size="32">
            <Microphone v-if="store.voiceStatus === 'idle'" />
            <Loading v-else-if="store.voiceStatus === 'recording'" />
            <Check v-else />
          </el-icon>
        </el-button>
        <p class="voice-hint">
          {{ store.voiceStatus === 'idle' ? '点击开始录音' : store.voiceStatus === 'recording' ? '录音中...' : '点击重新录音' }}
        </p>
      </div>
      <el-input
        v-if="store.voiceStatus === 'done'"
        v-model="store.voiceText" type="textarea" :rows="6"
        placeholder="语音转换文本..."
        class="voice-textarea"
      />
    </div>

    <!-- 手动模式 -->
    <div v-else class="manual-section">
      <el-card shadow="hover" class="topic-results-card">
        <template #header><span class="card-title">议题结果</span></template>
        <div v-for="t in store.topicResults" :key="t.id" class="topic-result-row">
          <span class="topic-label">{{ t.text }}</span>
          <el-radio-group v-model="t.result" size="small">
            <el-radio-button value="达成" style="--el-color-primary: #67C23A">✅ 达成</el-radio-button>
            <el-radio-button value="部分达成" style="--el-color-primary: #E6A23C">⚠️ 部分</el-radio-button>
            <el-radio-button value="未达成" style="--el-color-primary: #F56C6C">❌ 未达成</el-radio-button>
          </el-radio-group>
        </div>
      </el-card>
    </div>

    <!-- 客户表态 + 关系温度（两侧面板共用） -->
    <el-row :gutter="16" class="sentiment-row">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span class="card-title">客户表态</span></template>
          <div class="tag-group">
            <el-tag
              v-for="a in attitudes" :key="a.value"
              :type="store.customerAttitude === a.value ? '' : 'info'"
              :color="store.customerAttitude === a.value ? a.color : ''"
              :effect="store.customerAttitude === a.value ? 'dark' : 'plain'"
              size="large" class="clickable-tag"
              @click="store.customerAttitude = a.value"
            >
              {{ a.label }}
            </el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header><span class="card-title">关系温度</span></template>
          <div class="tag-group">
            <el-tag
              v-for="t in trends" :key="t.value"
              :type="store.relationTrend === t.value ? 'warning' : 'info'"
              :effect="store.relationTrend === t.value ? 'dark' : 'plain'"
              size="large" class="clickable-tag"
              @click="store.relationTrend = t.value"
            >
              <el-icon><component :is="t.icon" /></el-icon>
              {{ t.label }}
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 底部按钮 -->
    <div class="bottom-bar">
      <el-button size="large" @click="emit('prev')">上一步</el-button>
      <el-button type="primary" size="large" @click="emit('next')">
        生成AI纪要 <el-icon><MagicStick /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.record-screen { max-width: 900px; margin: 0 auto; }
.mode-tabs { text-align: center; margin-bottom: 24px; }
.voice-section .voice-btn-area { text-align: center; padding: 40px 0; }
.voice-hint { margin-top: 12px; color: #909399; font-size: 14px; }
.voice-textarea { margin-top: 16px; }
.card-title { font-size: 15px; font-weight: 600; }
.topic-results-card { margin-bottom: 16px; }
.topic-result-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid #f0f0f0;
  .topic-label { font-size: 14px; flex: 1; margin-right: 16px; }
}
.sentiment-row { margin-bottom: 20px; }
.tag-group { display: flex; gap: 12px; flex-wrap: wrap; }
.clickable-tag { cursor: pointer; }
.bottom-bar { display: flex; justify-content: center; gap: 16px; padding: 20px 0; }
</style>
