<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

interface MenuItem {
  path: string
  title: string
  icon: string
}

const menuItems: MenuItem[] = [
  { path: '/dashboard', title: '运营数据驾驶舱', icon: 'Odometer' },
  { path: '/customers', title: '客户列表', icon: 'User' },
  { path: '/bidding', title: '招投标管理', icon: 'Document' },
  { path: '/projects', title: '项目管理', icon: 'List' },
  { path: '/relationships', title: '关系维护', icon: 'Connection' },
  { path: '/contracts', title: '合同管理', icon: 'Tickets' },
  { path: '/acceptance', title: '验收管理', icon: 'Checked' },
  { path: '/ltc', title: 'LTC全链路', icon: 'TrendCharts' },
  { path: '/export', title: '数据导出', icon: 'Download' },
  { path: '/ai-reports', title: '工作总结', icon: 'EditPen' },
  { path: '/knowledge', title: '知识库管理', icon: 'Collection' },
  { path: '/settings', title: '系统设置', icon: 'Setting' },
]

const activeMenu = computed(() => {
  // 客户详情页也高亮客户列表
  if (route.path.startsWith('/customers')) return '/customers'
  return route.path
})

function navigateTo(path: string) {
  router.push(path)
}
</script>

<template>
  <div class="sidebar-container">
    <div class="sidebar-logo">
      <div class="logo-icon">
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
          <rect width="28" height="28" rx="8" fill="url(#logo-grad)"/>
          <path d="M7 14l4 4 10-10" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
          <defs><linearGradient id="logo-grad" x1="0" y1="0" x2="28" y2="28"><stop stop-color="#3b82f6"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>
        </svg>
      </div>
      <span v-show="!appStore.sidebarCollapsed" class="logo-text">AI CRM</span>
    </div>

    <el-menu
      :default-active="activeMenu"
      :collapse="appStore.sidebarCollapsed"
      background-color="var(--sidebar-bg)"
      text-color="#94a3b8"
      active-text-color="#fff"
      class="sidebar-menu"
      router
    >
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path" @click="navigateTo(item.path)">
        <el-icon><component :is="item.icon" /></el-icon>
        <template #title>{{ item.title }}</template>
      </el-menu-item>
    </el-menu>

    <div class="sidebar-collapse" @click="appStore.toggleSidebar()">
      <el-icon :size="18"><DArrowLeft v-if="!appStore.sidebarCollapsed" /><DArrowRight v-else /></el-icon>
    </div>
  </div>
</template>

<style scoped lang="scss">
.sidebar-container { display: flex; flex-direction: column; height: 100%; background: var(--sidebar-bg); }

.sidebar-logo {
  height: 64px; display: flex; align-items: center; justify-content: center; gap: 12px;
  border-bottom: 1px solid rgba(255,255,255,0.06); flex-shrink: 0;
  .logo-text { color: #fff; font-size: 18px; font-weight: 700; letter-spacing: -0.02em; white-space: nowrap; }
}

.sidebar-menu {
  flex: 1; border-right: none; overflow-y: auto; overflow-x: hidden; padding: 8px 0;
  .el-menu-item {
    margin: 2px 8px; border-radius: 8px; height: 44px; line-height: 44px;
    font-size: 13px; letter-spacing: -0.01em;
    transition: all 0.2s var(--ease-spring);
    &:hover { background: var(--sidebar-hover) !important; }
    &.is-active { background: var(--sidebar-active) !important; color: #fff !important; border-right: none; }
  }
}

.sidebar-collapse {
  height: 40px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #64748b; border-top: 1px solid rgba(255,255,255,0.06); flex-shrink: 0;
  transition: color 0.2s;
  &:hover { color: #94a3b8; }
}
</style>
