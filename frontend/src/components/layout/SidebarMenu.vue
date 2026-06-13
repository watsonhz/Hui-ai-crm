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
    <!-- Logo 区域 -->
    <div class="sidebar-logo">
      <el-icon :size="24" color="#409EFF"><Cpu /></el-icon>
      <span v-show="!appStore.sidebarCollapsed" class="logo-text">AI CRM</span>
    </div>

    <!-- 菜单 -->
    <el-menu
      :default-active="activeMenu"
      :collapse="appStore.sidebarCollapsed"
      background-color="#1d1e2c"
      text-color="#a6a7b3"
      active-text-color="#fff"
      class="sidebar-menu"
      router
    >
      <el-menu-item
        v-for="item in menuItems"
        :key="item.path"
        :index="item.path"
        @click="navigateTo(item.path)"
      >
        <el-icon><component :is="item.icon" /></el-icon>
        <template #title>{{ item.title }}</template>
      </el-menu-item>
    </el-menu>

    <!-- 底部折叠按钮 -->
    <div class="sidebar-collapse" @click="appStore.toggleSidebar()">
      <el-icon :size="18">
        <DArrowLeft v-if="!appStore.sidebarCollapsed" />
        <DArrowRight v-else />
      </el-icon>
    </div>
  </div>
</template>

<style scoped lang="scss">
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-logo {
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;

  .logo-text {
    color: #fff;
    font-size: 16px;
    font-weight: 700;
    white-space: nowrap;
  }
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  overflow-y: auto;
  overflow-x: hidden;

  .el-menu-item {
    &:hover {
      background-color: rgba(255, 255, 255, 0.05) !important;
    }
    &.is-active {
      background-color: #409EFF !important;
    }
  }
}

.sidebar-collapse {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #a6a7b3;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  transition: color 0.2s;
  flex-shrink: 0;

  &:hover {
    color: #fff;
  }
}
</style>
