<script setup lang="ts">
import SidebarMenu from './SidebarMenu.vue'
import HeaderBreadcrumb from './HeaderBreadcrumb.vue'
import { useAppStore } from '@/stores/app'

const appStore = useAppStore()
</script>

<template>
  <el-container class="app-layout">
    <!-- 侧边栏 -->
    <el-aside :width="appStore.sidebarWidth" class="app-aside">
      <SidebarMenu />
    </el-aside>

    <!-- 右侧主体 -->
    <el-container>
      <!-- 顶栏 -->
      <el-header class="app-header">
        <HeaderBreadcrumb />
      </el-header>

      <!-- 内容区 -->
      <el-main class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped lang="scss">
.app-layout {
  height: 100vh;
  overflow: hidden;
}

.app-aside {
  background-color: #1d1e2c;
  transition: width 0.3s ease;
  overflow-x: hidden;
  flex-shrink: 0;
}

.app-header {
  height: 56px !important;
  background: #fff;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
  padding: 0 20px;
  flex-shrink: 0;
}

.app-main {
  background: #f5f6fa;
  overflow-y: auto;
  padding: 20px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
