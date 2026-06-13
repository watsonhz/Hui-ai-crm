<script setup lang="ts">
import { onMounted } from 'vue'
import { useVisitStore } from '@/stores/visit'
import { fetchVisit } from '@/api/visit'
import VisitPrepare from '@/components/visit/VisitPrepare.vue'
import VisitRecord from '@/components/visit/VisitRecord.vue'
import VisitSummary from '@/components/visit/VisitSummary.vue'

const store = useVisitStore()

const screens = [
  { key: 1 as const, label: '准备卡', icon: 'DocumentChecked' },
  { key: 2 as const, label: '快速记录', icon: 'Edit' },
  { key: 3 as const, label: 'AI 纪要', icon: 'MagicStick' },
]

onMounted(async () => {
  try {
    const data = await fetchVisit(1)
    store.setVisitData(data)
  } catch {
    // 使用演示数据
    store.setVisitData({
      customerId: 1,
      customerName: '中科曙光信息产业股份有限公司',
      stage: '第2次',
      visitTime: '2026-06-15 14:00',
      location: '总部大楼 18F 会议室',
      ourAttendees: '李经理（销售总监）、王工（技术负责人）',
      customerAttendees: '张总（CIO）、刘工（运维负责人）',
      purpose: '年度IT运维平台升级方案汇报与商务沟通',
      contacts: '张总: 13800001111 / 刘工: 13800002222',
      alerts: [
        { type: 'warning', text: '上次拜访遗留：合同付款条款待法务确认（已超5个工作日）' },
        { type: 'danger', text: '竞争对手华为云已于上周拜访过张总' },
        { type: 'info', text: '最近3个月采购预算审批已通过，金额约800万' },
      ],
      actionItems: [
        { id: 1, content: '发邮件确认本次拜访议程和时间', done: true, due: '2026-06-13', assignee: '李经理', priority: 'P0' },
        { id: 2, content: '准备技术方案演示PPT（IT运维平台v3.2）', done: true, due: '2026-06-13', assignee: '王工', priority: 'P1' },
        { id: 3, content: '提前发送会议资料给张总助理', done: false, due: '2026-06-14', assignee: '李经理', priority: 'P0' },
        { id: 4, content: '准备商务报价方案（A/B两套）', done: false, due: '2026-06-14', assignee: '李经理', priority: 'P1' },
      ],
      topics: [
        { id: 1, text: '年度运维平台升级方案汇报（核心）' },
        { id: 2, text: '上半年服务报告回顾与客户满意度确认' },
        { id: 3, text: '下一步AI运维能力引入探讨' },
        { id: 4, text: '合同续签时间节点沟通' },
        { id: 5, text: '技术团队驻场POC安排' },
      ],
    })
  }
})
</script>

<template>
  <div class="relationships-page">
    <!-- 步骤条 -->
    <el-steps :active="store.currentScreen" align-center finish-status="success" class="visit-steps">
      <el-step v-for="s in screens" :key="s.key" :title="s.label" />
    </el-steps>

    <!-- 屏切换 -->
    <div class="screen-switcher">
      <el-radio-group v-model="store.currentScreen" size="large">
        <el-radio-button v-for="s in screens" :key="s.key" :value="s.key">
          <el-icon><component :is="s.icon" /></el-icon>
          {{ s.label }}
        </el-radio-button>
      </el-radio-group>
    </div>

    <!-- 三屏内容 -->
    <VisitPrepare v-if="store.currentScreen === 1" @next="store.nextScreen()" />
    <VisitRecord v-if="store.currentScreen === 2" @next="store.nextScreen()" @prev="store.prevScreen()" />
    <VisitSummary v-if="store.currentScreen === 3" @prev="store.prevScreen()" />
  </div>
</template>

<style scoped lang="scss">
.relationships-page { max-width: 1400px; margin: 0 auto; }
.visit-steps { margin-bottom: 24px; }
.screen-switcher { text-align: center; margin-bottom: 24px; }
</style>
