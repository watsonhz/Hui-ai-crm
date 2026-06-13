/** 5次拜访 — 类型定义 */

export interface ActionItem {
  id: number
  content: string
  done: boolean
  due: string
  assignee: string
  priority: 'P0' | 'P1' | 'P2'
}

export interface Alert {
  type: 'danger' | 'warning' | 'info'
  text: string
}

export interface VisitInfo {
  customerId: number
  customerName: string
  stage: '第1次' | '第2次' | '第3次' | '第4次' | '第5次'
  visitTime: string
  location: string
  ourAttendees: string
  customerAttendees: string
  purpose: string
  contacts: string
}

export interface Topic {
  id: number
  text: string
  editable: boolean
}

export interface TopicResult {
  id: number
  text: string
  result: '达成' | '部分达成' | '未达成'
}

export type CustomerAttitude = '积极' | '观望' | '抵触'
export type RelationTrend = '升温' | '稳定' | '降温'

export interface VisitRecord {
  mode: 'voice' | 'manual'
  voiceText: string
  voiceStatus: 'idle' | 'recording' | 'done'
  topicResults: TopicResult[]
  customerAttitude: CustomerAttitude | null
  relationTrend: RelationTrend | null
}

export interface VisitMinutes {
  content: string
  updatedAt: string
}

export interface VisitScreen {
  screen: 1 | 2 | 3
  completed: boolean
}
