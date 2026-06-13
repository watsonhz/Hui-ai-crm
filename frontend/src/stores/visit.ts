import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type {
  VisitInfo, Alert, ActionItem, Topic, TopicResult,
  CustomerAttitude, RelationTrend, VisitMinutes,
} from '@/types/visit'

export const useVisitStore = defineStore('visit', () => {
  // ---- 屏1: 准备卡 ----
  const visitInfo = ref<VisitInfo>({
    customerId: 0, customerName: '', stage: '第1次',
    visitTime: '', location: '', ourAttendees: '', customerAttendees: '',
    purpose: '', contacts: '',
  })
  const alerts = ref<Alert[]>([])
  const actionItems = ref<ActionItem[]>([])
  const topics = ref<Topic[]>([])

  // ---- 屏2: 快速记录 ----
  const recordMode = ref<'voice' | 'manual'>('voice')
  const voiceText = ref('')
  const voiceStatus = ref<'idle' | 'recording' | 'done'>('idle')
  const topicResults = ref<TopicResult[]>([])
  const customerAttitude = ref<CustomerAttitude | null>(null)
  const relationTrend = ref<RelationTrend | null>(null)

  // ---- 屏3: AI 纪要 ----
  const minutes = ref<VisitMinutes>({ content: '', updatedAt: '' })

  // ---- 屏幕导航 ----
  const currentScreen = ref<1 | 2 | 3>(1)

  const unfinishedActions = computed(() => actionItems.value.filter(a => !a.done))

  function setVisitData(data: any) {
    visitInfo.value = {
      customerId: data.customerId || 0,
      customerName: data.customerName || '',
      stage: data.stage || '第1次',
      visitTime: data.visitTime || '',
      location: data.location || '',
      ourAttendees: data.ourAttendees || '',
      customerAttendees: data.customerAttendees || '',
      purpose: data.purpose || '',
      contacts: data.contacts || '',
    }
    alerts.value = data.alerts || []
    actionItems.value = data.actionItems || []
    topics.value = (data.topics || []).map((t: any) => ({ ...t, editable: false }))
    if (data.minutes) {
      minutes.value = { content: data.minutes, updatedAt: new Date().toISOString() }
    }
    // init topic results for screen 2
    topicResults.value = (data.topics || []).map((t: any) => ({
      id: t.id, text: t.text, result: '达成' as const,
    }))
  }

  function goToScreen(screen: 1 | 2 | 3) {
    currentScreen.value = screen
  }

  function nextScreen() {
    if (currentScreen.value < 3) currentScreen.value++
  }

  function prevScreen() {
    if (currentScreen.value > 1) currentScreen.value--
  }

  return {
    visitInfo, alerts, actionItems, topics, unfinishedActions,
    recordMode, voiceText, voiceStatus, topicResults, customerAttitude, relationTrend,
    minutes, currentScreen,
    setVisitData, goToScreen, nextScreen, prevScreen,
  }
})
