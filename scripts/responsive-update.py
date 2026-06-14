import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('106.55.106.85', username='root', password='Admin@90088*', timeout=15)
sftp = client.open_sftp()

# AppStore
with sftp.open('/www/wwwroot/202606AICRM/frontend/src/stores/app.ts', 'w') as f:
    f.write('''import { defineStore } from "pinia"
import { ref, computed } from "vue"

export const useAppStore = defineStore("app", () => {
  const sidebarCollapsed = ref(false)
  const currentPageTitle = ref("")
  const isMobile = ref(typeof window !== "undefined" ? window.innerWidth < 768 : false)
  const isTablet = ref(typeof window !== "undefined" ? (window.innerWidth >= 768 && window.innerWidth < 1024) : false)
  const mobileMenuOpen = ref(false)

  const sidebarWidth = computed(() => {
    if (isMobile.value) return "0px"
    if (isTablet.value) return "64px"
    return sidebarCollapsed.value ? "64px" : "220px"
  })

  function toggleSidebar() {
    if (isMobile.value) {
      mobileMenuOpen.value = !mobileMenuOpen.value
    } else {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }
  }

  function closeMobileMenu() { mobileMenuOpen.value = false }

  function setPageTitle(title: string) {
    currentPageTitle.value = title
    document.title = title + " - AI CRM"
  }

  if (typeof window !== "undefined") {
    window.addEventListener("resize", () => {
      isMobile.value = window.innerWidth < 768
      isTablet.value = window.innerWidth >= 768 && window.innerWidth < 1024
      if (!isMobile.value) mobileMenuOpen.value = false
    })
  }

  return { sidebarCollapsed, currentPageTitle, sidebarWidth, isMobile, isTablet, mobileMenuOpen, toggleSidebar, closeMobileMenu, setPageTitle }
})'''.encode())

# AppLayout
with sftp.open('/www/wwwroot/202606AICRM/frontend/src/components/layout/AppLayout.vue', 'w') as f:
    f.write('''<script setup lang="ts">
import SidebarMenu from "./SidebarMenu.vue"
import HeaderBreadcrumb from "./HeaderBreadcrumb.vue"
import { useAppStore } from "@/stores/app"
const appStore = useAppStore()
</script>

<template>
  <el-container class="app-layout">
    <div v-if="appStore.isMobile && appStore.mobileMenuOpen" class="mobile-overlay" @click="appStore.closeMobileMenu()" />
    <el-aside :width="appStore.sidebarWidth" class="app-aside" :class="{ 'mobile-open': appStore.mobileMenuOpen }">
      <SidebarMenu />
    </el-aside>
    <el-container>
      <el-header class="app-header">
        <div v-if="appStore.isMobile" class="mobile-toggle" @click="appStore.toggleSidebar()">
          <el-icon :size="22"><component :is="appStore.mobileMenuOpen ? 'Fold' : 'Expand'" /></el-icon>
        </div>
        <HeaderBreadcrumb />
      </el-header>
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
.app-layout { height: 100vh; overflow: hidden; }
.mobile-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 99; }
.app-aside {
  background-color: #1d1e2c; transition: width 0.3s ease; overflow-x: hidden; flex-shrink: 0; z-index: 100;
  &.mobile-open { position: fixed; left: 0; top: 0; bottom: 0; width: 220px !important; z-index: 101; }
}
.mobile-toggle { margin-right: 12px; cursor: pointer; color: #333; display: flex; align-items: center; }
.app-header { height: 56px !important; background: #fff; border-bottom: 1px solid #e8e8e8; display: flex; align-items: center; padding: 0 16px; flex-shrink: 0; }
.app-main { background: #f5f6fa; overflow-y: auto; padding: 16px; }
@media (max-width: 767px) {
  .app-header { padding: 0 10px; }
  .app-main { padding: 10px; }
}
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>'''.encode())

# SidebarMenu
with sftp.open('/www/wwwroot/202606AICRM/frontend/src/components/layout/SidebarMenu.vue', 'w') as f:
    f.write('''<script setup lang="ts">
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAppStore } from "@/stores/app"

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

const menuItems = [
  { path: "/dashboard", title: "数据驾驶舱", icon: "Odometer" },
  { path: "/customers", title: "客户列表", icon: "User" },
  { path: "/bidding", title: "招投标管理", icon: "Document" },
  { path: "/projects", title: "项目管理", icon: "List" },
  { path: "/relationships", title: "关系维护", icon: "Connection" },
  { path: "/contracts", title: "合同管理", icon: "Tickets" },
  { path: "/acceptance", title: "验收管理", icon: "Checked" },
  { path: "/ltc", title: "LTC全链路", icon: "TrendCharts" },
  { path: "/ai-reports", title: "工作总结", icon: "EditPen" },
  { path: "/knowledge", title: "知识库管理", icon: "Collection" },
  { path: "/settings", title: "系统设置", icon: "Setting" },
]

const activeMenu = computed(() => route.path.startsWith("/customers") ? "/customers" : route.path)

function navigateTo(path: string) {
  router.push(path)
  if (appStore.isMobile) appStore.closeMobileMenu()
}
</script>

<template>
  <div class="sidebar-container">
    <div class="sidebar-logo">
      <el-icon :size="24" color="#409EFF"><Cpu /></el-icon>
      <span v-show="!appStore.sidebarCollapsed || appStore.isMobile" class="logo-text">AI CRM</span>
    </div>
    <el-menu
      :default-active="activeMenu"
      :collapse="appStore.sidebarCollapsed && !appStore.isMobile"
      background-color="#1d1e2c" text-color="#a6a7b3" active-text-color="#fff"
      class="sidebar-menu"
    >
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path" @click="navigateTo(item.path)">
        <el-icon><component :is="item.icon" /></el-icon>
        <template #title>{{ item.title }}</template>
      </el-menu-item>
    </el-menu>
    <div v-if="!appStore.isMobile" class="sidebar-collapse" @click="appStore.toggleSidebar()">
      <el-icon :size="18">
        <DArrowLeft v-if="!appStore.sidebarCollapsed" /><DArrowRight v-else />
      </el-icon>
    </div>
  </div>
</template>

<style scoped lang="scss">
.sidebar-container { display: flex; flex-direction: column; height: 100%; }
.sidebar-logo { height: 56px; display: flex; align-items: center; justify-content: center; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.06); flex-shrink: 0; .logo-text { color: #fff; font-size: 16px; font-weight: 700; white-space: nowrap; } }
.sidebar-menu { flex: 1; border-right: none; overflow-y: auto; overflow-x: hidden; .el-menu-item { &:hover { background-color: rgba(255,255,255,0.05) !important; } &.is-active { background-color: #409EFF !important; } } }
.sidebar-collapse { height: 40px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #a6a7b3; border-top: 1px solid rgba(255,255,255,0.06); transition: color 0.2s; flex-shrink: 0; &:hover { color: #fff; } }
</style>'''.encode())

sftp.close()

# Rebuild
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/202606AICRM/frontend && npx vite build --base=/aicrm/ 2>&1 | tail -6')
print('Build:', stdout.read().decode())
err = stderr.read().decode()
if err and 'error' in err.lower():
    print('ERR:', err[:300])
elif err:
    print('Warn:', err[:200])

# Verify
stdin, stdout, stderr = client.exec_command('curl -sk -o /dev/null -w "%{http_code}" https://localhost/aicrm/')
print('Verify:', stdout.read().decode())

client.close()
print('Done')
