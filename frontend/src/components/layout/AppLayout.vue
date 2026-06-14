<script setup lang="ts">
import SidebarMenu from './SidebarMenu.vue'
import HeaderBreadcrumb from './HeaderBreadcrumb.vue'
import MobileBottomNav from './MobileBottomNav.vue'
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
      <el-main id="main-content" class="app-main" tabindex="-1">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>

    <MobileBottomNav />
  </el-container>
</template>

<style scoped lang="scss">
.app-layout { height: 100vh; overflow: hidden; }
.app-aside { background: var(--sidebar-bg); transition: width 0.3s var(--ease-spring); overflow-x: hidden; flex-shrink: 0; }

.app-header {
  height: 64px !important;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--color-border);
  display: flex; align-items: center; padding: 0 24px; flex-shrink: 0;
}

.app-main {
  background: var(--color-bg);
  overflow-y: auto; padding: 24px;
}
</style>
