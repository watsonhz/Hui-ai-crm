<script setup lang="ts">
import { ref, computed } from 'vue'

type Screen = 1 | 2 | 3
const currentScreen = ref<Screen>(1)
const screens = [
  { key: 1, label: '准备卡', icon: 'DocumentChecked' },
  { key: 2, label: '快速记录', icon: 'Edit' },
  { key: 3, label: 'AI 纪要', icon: 'MagicStick' },
]

// ---- 屏1 准备卡数据 ----
const visitInfo = ref({
  customerName: '中科曙光信息产业股份有限公司',
  contactPerson: '张总（CIO）',
  visitDate: '2026-06-15 14:00',
  location: '总部大楼 18F 会议室',
  purpose: '年度IT运维平台升级方案汇报',
})

const alerts = ref([
  { type: 'warning', text: '上次拜访遗留：合同付款条款待法务确认（已超5个工作日）' },
  { type: 'info', text: '最近3个月采购预算审批已通过，金额约800万' },
  { type: 'danger', text: '竞争对手华为云已于上周拜访过张总' },
])

const lastActions = ref([
  { done: false, content: '发邮件确认本次拜访议程和时间', due: '2026-06-13' },
  { done: true, content: '准备技术方案演示PPT（IT运维平台v3.2）', due: '2026-06-13' },
  { done: false, content: '提前发送会议资料给张总助理', due: '2026-06-14' },
  { done: true, content: '准备商务报价方案（A/B两套）', due: '2026-06-14' },
])

const suggestedTopics = ref([
  '年度运维平台升级方案汇报（核心）',
  '上半年服务报告回顾与客户满意度确认',
  '下一步AI运维能力引入探讨',
  '合同续签时间节点沟通',
])

// ---- 屏2 快速记录 ----
const recordMode = ref<'voice' | 'manual'>('voice')
const voiceStatus = ref<'idle' | 'recording' | 'done'>('idle')
const voiceText = ref('')
const manualChecks = ref([
  { id: 1, label: '客户对方案整体满意', category: '反馈', checked: false },
  { id: 2, label: '客户要求增加AI功能模块', category: '需求', checked: false },
  { id: 3, label: '价格需要再优惠5%', category: '商务', checked: false },
  { id: 4, label: '项目时间可提前1个月', category: '进度', checked: false },
  { id: 5, label: '需要安排技术团队驻场', category: '需求', checked: false },
  { id: 6, label: '客户提了竞争对手的优势点', category: '竞争', checked: false },
  { id: 7, label: '合同条款需法务介入', category: '法务', checked: false },
  { id: 8, label: '下次拜访约在下周三', category: '跟进', checked: false },
])

function toggleVoice() {
  if (voiceStatus.value === 'idle') {
    voiceStatus.value = 'recording'
    // Simulate recording
    setTimeout(() => {
      voiceStatus.value = 'done'
      voiceText.value = '今天拜访中科曙光张总，整体效果很好。张总对我们的IT运维平台v3.2方案非常认可，特别对AI运维能力模块表示强烈兴趣。商务方面，客户希望价格再优惠5%，我们初步沟通后认为可在3%范围内让步。客户同意将项目启动时间提前1个月，这对我们排期是利好。下一步需要安排技术团队驻场做POC演示。'
    }, 3000)
  } else {
    voiceStatus.value = 'idle'
    voiceText.value = ''
  }
}

// ---- 屏3 AI纪要 ----
const aiMinutes = ref(`# 拜访纪要：中科曙光 — 张总（CIO）

**时间：** 2026-06-15 14:00-15:30
**地点：** 总部大楼 18F 会议室
**我方参会：** 李经理、王技术总监
**客户参会：** 张总（CIO）、刘工（运维负责人）

## 一、会议背景
本次拜访为年度IT运维平台升级项目的第二次正式沟通，在初次建立信任的基础上，本次重点汇报v3.2版本技术方案及商务报价。

## 二、核心内容
1. **方案汇报**：王总监汇报了IT运维平台v3.2升级方案，重点展示了AI运维能力模块（智能告警、自动工单、故障预测）。
2. **客户反馈**：张总对方案整体评价很高，特别对AI运维模块表示"这是我们需要的能力"。刘工对技术细节提出了几个具体建议。
3. **商务沟通**：李经理提交了A/B两套报价方案。

## 三、关键决策
- 客户确认项目优先级，同意提前1个月启动
- 价格需要再沟通，客户期望优惠5%
- 下一步安排技术团队驻场POC`)

const actionItems = ref([
  { priority: 'P0', text: '发正式报价函（含3%优惠方案）给张总', assignee: '李经理', due: '2026-06-16', done: false },
  { priority: 'P0', text: '安排技术团队驻场POC计划（2周）', assignee: '王总监', due: '2026-06-17', done: false },
  { priority: 'P1', text: '更新CRM系统客户阶段为「商务谈判」', assignee: '系统自动', due: '2026-06-15', done: true },
  { priority: 'P1', text: '刘工反馈的3个技术建议纳入v3.2.1迭代', assignee: '王总监', due: '2026-06-20', done: false },
  { priority: 'P2', text: '发送感谢邮件并附会议纪要', assignee: '李经理', due: '2026-06-16', done: true },
])
</script>

<template>
  <div class="relationships-page">
    <!-- 顶部步骤条 -->
    <el-steps :active="currentScreen" align-center finish-status="success" class="visit-steps">
      <el-step v-for="s in screens" :key="s.key" :title="s.label" />
    </el-steps>

    <!-- 屏切换按钮 -->
    <div class="screen-switcher">
      <el-radio-group v-model="currentScreen" size="large">
        <el-radio-button v-for="s in screens" :key="s.key" :value="s.key">
          <el-icon><component :is="s.icon" /></el-icon>
          {{ s.label }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <!-- ============ 屏1：准备卡 ============ -->
    <div v-if="currentScreen === 1" class="screen-content">
      <!-- 告警区 -->
      <el-alert
        v-for="(alert, i) in alerts" :key="i"
        :title="alert.text" :type="alert.type as any"
        :closable="false" show-icon class="alert-item"
      />

      <!-- 核心信息 -->
      <el-card shadow="hover" class="info-card">
        <template #header><span class="card-title">拜访信息</span></template>
        <el-descriptions :column="2" border size="default">
          <el-descriptions-item label="客户名称" :span="2">{{ visitInfo.customerName }}</el-descriptions-item>
          <el-descriptions-item label="联系人">{{ visitInfo.contactPerson }}</el-descriptions-item>
          <el-descriptions-item label="拜访时间">{{ visitInfo.visitDate }}</el-descriptions-item>
          <el-descriptions-item label="地点" :span="2">{{ visitInfo.location }}</el-descriptions-item>
          <el-descriptions-item label="拜访目的" :span="2">{{ visitInfo.purpose }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-row :gutter="16">
        <!-- 上次待办 -->
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header><span class="card-title">待办事项</span></template>
            <div v-for="item in lastActions" :key="item.content" class="todo-item">
              <el-checkbox v-model="item.done" :label="item.content" disabled />
              <el-tag size="small" :type="item.done ? 'success' : 'warning'">
                {{ item.done ? '已完成' : item.due }}
              </el-tag>
            </div>
          </el-card>
        </el-col>

        <!-- 建议议题 -->
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header><span class="card-title">建议议题</span></template>
            <ul class="topic-list">
              <li v-for="(topic, i) in suggestedTopics" :key="i">
                <el-icon color="#409EFF"><ChatDotRound /></el-icon>
                {{ topic }}
              </li>
            </ul>
          </el-card>
        </el-col>
      </el-row>

      <!-- 可展开详情（历史拜访记录） -->
      <el-collapse class="detail-collapse">
        <el-collapse-item title="展开历史拜访记录 (最近5次)" name="1">
          <el-timeline>
            <el-timeline-item timestamp="2026-06-01" placement="top">
              初次拜访，了解客户IT运维现状，建立信任关系
            </el-timeline-item>
            <el-timeline-item timestamp="2026-05-15" placement="top">
              电话沟通，确认年度运维平台升级需求
            </el-timeline-item>
            <el-timeline-item timestamp="2026-04-20" placement="top">
              通过渠道介绍初次接触张总助理
            </el-timeline-item>
          </el-timeline>
        </el-collapse-item>
      </el-collapse>
    </div>

    <!-- ============ 屏2：快速记录 ============ -->
    <div v-if="currentScreen === 2" class="screen-content">
      <div class="record-tabs">
        <el-radio-group v-model="recordMode">
          <el-radio-button value="voice">🎤 语音模式</el-radio-button>
          <el-radio-button value="manual">📋 手动勾选</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 语音模式 -->
      <div v-if="recordMode === 'voice'" class="voice-area">
        <div class="voice-indicator">
          <el-button
            :type="voiceStatus === 'recording' ? 'danger' : 'primary'"
            size="large" circle @click="toggleVoice"
          >
            <el-icon :size="28">
              <Microphone v-if="voiceStatus === 'idle'" />
              <Loading v-else-if="voiceStatus === 'recording'" />
              <Check v-else />
            </el-icon>
          </el-button>
          <p class="voice-hint">
            {{ voiceStatus === 'idle' ? '点击开始录音' : voiceStatus === 'recording' ? '录音中...' : '点击重新录音' }}
          </p>
        </div>
        <el-input
          v-model="voiceText" type="textarea" :rows="8"
          placeholder="语音转文字结果将显示在这里..."
          v-if="voiceStatus === 'done'"
        />
      </div>

      <!-- 手动勾选 -->
      <div v-else class="manual-area">
        <el-checkbox-group>
          <div v-for="item in manualChecks" :key="item.id" class="manual-item">
            <el-checkbox v-model="item.checked">
              <el-tag size="small" type="info">{{ item.category }}</el-tag>
              {{ item.label }}
            </el-checkbox>
          </div>
        </el-checkbox-group>
      </div>
    </div>

    <!-- ============ 屏3：AI纪要 ============ -->
    <div v-if="currentScreen === 3" class="screen-content">
      <el-row :gutter="16" class="minutes-row">
        <!-- 左栏：纪要（可编辑） -->
        <el-col :span="14">
          <el-card shadow="hover">
            <template #header>
              <span class="card-title">AI 生成纪要</span>
              <el-button type="primary" size="small" link style="float:right">重新生成</el-button>
            </template>
            <el-input
              v-model="aiMinutes" type="textarea" :rows="22"
              placeholder="AI 生成的会议纪要..."
            />
          </el-card>
        </el-col>

        <!-- 右栏：行动项 -->
        <el-col :span="10">
          <el-card shadow="hover">
            <template #header><span class="card-title">行动项</span></template>
            <div v-for="item in actionItems" :key="item.text" class="action-item">
              <el-checkbox v-model="item.done">
                <el-tag :type="item.priority === 'P0' ? 'danger' : item.priority === 'P1' ? 'warning' : 'info'" size="small">
                  {{ item.priority }}
                </el-tag>
                {{ item.text }}
              </el-checkbox>
              <div class="action-meta">
                <span>{{ item.assignee }}</span>
                <span>{{ item.due }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped lang="scss">
.relationships-page { max-width: 1400px; margin: 0 auto; }

.visit-steps { margin-bottom: 24px; }

.screen-switcher {
  text-align: center; margin-bottom: 24px;
  .el-radio-group { .el-radio-button { margin: 0 2px; } }
}

.screen-content { animation: fadeIn 0.3s ease; }

.alert-item { margin-bottom: 10px; }
.info-card { margin-bottom: 16px; }

.todo-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 0; border-bottom: 1px solid #f0f0f0;
  &:last-child { border-bottom: none; }
}

.topic-list {
  list-style: none; padding: 0;
  li {
    padding: 8px 0; display: flex; align-items: center; gap: 8px;
    font-size: 14px; border-bottom: 1px solid #f5f5f5;
  }
}

.detail-collapse { margin-top: 16px; }

.record-tabs { text-align: center; margin-bottom: 20px; }

.voice-area {
  .voice-indicator {
    text-align: center; padding: 40px 0;
    .voice-hint { margin-top: 12px; color: #909399; font-size: 14px; }
  }
}

.manual-area {
  .manual-item {
    padding: 10px 0; border-bottom: 1px solid #f5f5f5;
  }
}

.minutes-row { .el-card { height: 100%; } }

.action-item {
  padding: 10px 0; border-bottom: 1px solid #f0f0f0;
  .action-meta {
    display: flex; gap: 16px; margin-top: 4px; margin-left: 24px;
    font-size: 12px; color: #909399;
  }
}

.card-title { font-size: 15px; font-weight: 600; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
</style>
