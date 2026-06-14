<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const tabs = [
  { path: '/dashboard', label: '驾驶舱', icon: 'Odometer' },
  { path: '/customers', label: '客户', icon: 'User' },
  { path: '/relationships', label: '拜访', icon: 'Connection' },
  { path: '/contracts', label: '合同', icon: 'Tickets' },
  { path: '/settings', label: '设置', icon: 'Setting' },
]

function go(p: string) { router.push(p) }
</script>

<template>
  <nav class="mobile-nav">
    <div v-for="t in tabs" :key="t.path" class="nav-item" :class="{ active: route.path.startsWith(t.path) }" @click="go(t.path)">
      <el-icon :size="20"><component :is="t.icon" /></el-icon>
      <span>{{ t.label }}</span>
    </div>
  </nav>
</template>

<style scoped>
.mobile-nav {
  display: none;
  position: fixed; bottom: 0; left: 0; right: 0; z-index: 999;
  background: #fff; border-top: 1px solid #e8e8e8;
  padding: 4px 0 env(safe-area-inset-bottom, 8px);
  justify-content: space-around;
}
.nav-item {
  display: flex; flex-direction: column; align-items: center; gap: 2px;
  padding: 6px 12px; cursor: pointer; color: #909399; font-size: 11px;
  transition: color 0.2s;
}
.nav-item.active { color: #409EFF; }

@media (max-width: 768px) {
  .mobile-nav { display: flex; }
}
</style>
