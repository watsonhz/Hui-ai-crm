/** 拜访 API */

const BASE = '/api/v1/relationships'

export interface VisitResponse {
  id: number
  customerId: number
  stage: string
  visitTime: string
  location: string
  ourAttendees: string
  customerAttendees: string
  purpose: string
  contacts: string
  alerts: Array<{ type: string; text: string }>
  actionItems: Array<{
    id: number
    content: string
    done: boolean
    due: string
    assignee: string
    priority: string
  }>
  topics: Array<{ id: number; text: string }>
  minutes: string | null
}

export async function fetchVisit(customerId: number): Promise<VisitResponse> {
  const res = await fetch(`${BASE}/${customerId}/visits`)
  if (!res.ok) throw new Error(`获取拜访数据失败: ${res.status}`)
  return res.json()
}

export async function saveMinutes(customerId: number, minutes: string): Promise<void> {
  await fetch(`${BASE}/${customerId}/visits/minutes`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ minutes }),
  })
}

export async function updateActions(customerId: number, actions: Array<{ id: number; done: boolean }>): Promise<void> {
  await fetch(`${BASE}/${customerId}/visits/actions`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ actions }),
  })
}
