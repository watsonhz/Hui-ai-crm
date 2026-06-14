<script setup lang="ts">
import { ref } from 'vue'

interface Notification { id: number; title: string; category: string; time: string; read: boolean; icon: string }
const visible = ref(false)
const items = ref<Notification[]>([
  { id: 1, title: 'PC4 安全审查完成：TASK-001 通过', category: '审查', time: '10分钟前', read: false, icon: 'Checked' },
  { id: 2, title: 'PC5 QA报告：8/8 测试通过', category: 'QA', time: '30分钟前', read: false, icon: 'DataAnalysis' },
  { id: 3, title: 'PC1 下发新任务：TASK-025 PostgreSQL迁移', category: '任务', time: '1小时前', read: false, icon: 'Document' },
  { id: 4, title: '系统自动备份完成', category: '系统', time: '3小时前', read: true, icon: 'Setting' },
  { id: 5, title: '投标"智慧园区"状态变更：方案设计→投标中', category: '系统', time: '5小时前', read: true, icon: 'Tickets' },
])
const unreadCount = ref(items.value.filter(i => !i.read).length)
const catColors: Record<string, string> = { '系统': 'info', '任务': 'primary', '审查': 'warning', 'QA': 'success' }

function markAllRead() { items.value.forEach(i => i.read = true); unreadCount.value = 0 }
</script>

<template>
  <el-popover :visible="visible" placement="bottom-end" :width="380" trigger="click" @show="visible = true" @hide="visible = false">
    <template #reference>
      <el-badge :value="unreadCount" :max="99" :hidden="unreadCount === 0">
        <el-icon :size="20" style="cursor:pointer" @click="visible = !visible"><Bell /></el-icon>
      </el-badge>
    </template>

    <div class="notify-list">
      <div class="notify-header">
        <span>消息通知</span>
        <el-button size="small" text type="primary" @click="markAllRead">全部标为已读</el-button>
      </div>
      <div v-for="item in items" :key="item.id" class="notify-item" :class="{ unread: !item.read }">
        <el-icon :size="18"><component :is="item.icon" /></el-icon>
        <div class="notify-body">
          <p class="notify-title">{{ item.title }}</p>
          <div class="notify-meta">
            <el-tag :type="catColors[item.category]" size="small">{{ item.category }}</el-tag>
            <span>{{ item.time }}</span>
          </div>
        </div>
        <div v-if="!item.read" class="unread-dot" />
      </div>
    </div>
  </el-popover>
</template>

<style scoped>
.notify-list { max-height: 400px; overflow-y: auto; }
.notify-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 8px; border-bottom: 1px solid #eee; margin-bottom: 8px; font-weight: 600; }
.notify-item { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
.notify-item.unread { background: #f0f7ff; margin: 0 -12px; padding: 10px 12px; }
.notify-body { flex: 1; }
.notify-title { margin: 0; font-size: 13px; }
.notify-meta { display: flex; gap: 8px; align-items: center; margin-top: 4px; font-size: 12px; color: #909399; }
.unread-dot { width: 8px; height: 8px; border-radius: 50%; background: #409EFF; flex-shrink: 0; margin-top: 6px; }
</style>
