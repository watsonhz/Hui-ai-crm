import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('106.55.106.85', username='root', password='Admin@90088*', timeout=15)
sftp = client.open_sftp()

# === 1. Global Apple-style CSS ===
with sftp.open('/www/wwwroot/202606AICRM/frontend/src/assets/styles/global.scss', 'w') as f:
    f.write("""/* === HuiSmart Design — Apple-Inspired === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  --bg: #f5f5f7; --card: #fff; --sidebar: #fbfbfd;
  --text: #1d1d1f; --text2: #86868b; --text3: #6e6e73;
  --accent: #0071e3; --accent-hover: #0077ed;
  --border: rgba(0,0,0,0.06); --radius: 12px;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 12px 40px rgba(0,0,0,0.08);
  --ease: 0.35s cubic-bezier(0.25, 0.1, 0.25, 1);
}
* { box-sizing: border-box; }
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased; background: var(--bg); color: var(--text);
  letter-spacing: -0.01em;
}
html { scroll-behavior: smooth; }

.el-card {
  border-radius: 18px !important; border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-sm) !important; transition: all var(--ease) !important;
  background: var(--card) !important;
}
.el-card:hover { box-shadow: var(--shadow-md) !important; transform: translateY(-2px); }

.el-button {
  border-radius: 980px !important; font-weight: 500 !important;
  letter-spacing: -0.01em; transition: all var(--ease) !important; padding: 10px 22px !important;
}
.el-button--primary { background: var(--accent) !important; border-color: var(--accent) !important; }
.el-button--primary:hover { background: var(--accent-hover) !important; transform: scale(1.02); }

.el-input__wrapper {
  border-radius: 12px !important; box-shadow: var(--shadow-sm) !important;
  transition: all var(--ease) !important;
}
.el-input__wrapper:hover { box-shadow: var(--shadow-md) !important; }

.el-table {
  border-radius: 18px !important; overflow: hidden; font-size: 14px;
}
.el-table th { background: var(--bg) !important; font-weight: 600; color: var(--text); border: none !important; }
.el-table tr { transition: background 0.2s; }
.el-table tr:hover>td { background: rgba(0,113,227,0.03) !important; }

.el-menu { border-right: none !important; }
.el-menu-item {
  margin: 1px 8px; border-radius: 8px !important; transition: all 0.2s !important;
  font-size: 13px; font-weight: 440;
}
.el-menu-item:hover { background: rgba(0,0,0,0.04) !important; }

.el-dialog { border-radius: 24px !important; box-shadow: var(--shadow-lg) !important; }
.el-overlay { backdrop-filter: blur(12px); background: rgba(0,0,0,0.2) !important; }
.el-tag { border-radius: 980px !important; font-weight: 500; }
.el-pagination { font-weight: 500; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.4s cubic-bezier(0.4,0,0.2,1); }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(8px); }

.card-grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.12); border-radius: 3px; }

@media (max-width: 767px) {
  .el-card { border-radius: 14px !important; }
  .el-card:hover { transform: none; }
  .el-dialog { width: 95% !important; border-radius: 18px !important; }
  .card-grid { grid-template-columns: 1fr; }
}
""".encode())
print('Global CSS done')

# === 2. AppLayout ===
with sftp.open('/www/wwwroot/202606AICRM/frontend/src/components/layout/AppLayout.vue', 'w') as f:
    f.write("""<script setup lang="ts">
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
.mobile-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); backdrop-filter: blur(10px); z-index: 99; }
.app-aside {
  background: #fbfbfd; transition: width 0.4s cubic-bezier(0.25,0.1,0.25,1);
  overflow-x: hidden; flex-shrink: 0; z-index: 100;
  border-right: 1px solid rgba(0,0,0,0.05);
  &.mobile-open { position: fixed; left: 0; top: 0; bottom: 0; width: 260px !important; z-index: 101; }
}
.mobile-toggle { margin-right: 12px; cursor: pointer; color: #1d1d1f; display: flex; align-items: center; }
.app-header {
  height: 52px !important; background: rgba(255,255,255,0.75);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  display: flex; align-items: center; padding: 0 24px; flex-shrink: 0;
}
.app-main { background: #f5f5f7; overflow-y: auto; padding: 32px 36px; }
@media (max-width: 767px) { .app-header { padding: 0 14px; } .app-main { padding: 14px; } }
</style>""".encode())
print('AppLayout done')

# === 3. SidebarMenu ===
with sftp.open('/www/wwwroot/202606AICRM/frontend/src/components/layout/SidebarMenu.vue', 'w') as f:
    f.write("""<script setup lang="ts">
import { computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAppStore } from "@/stores/app"
import logoUrl from "@/assets/logo.png"

const router = useRouter(); const route = useRoute(); const appStore = useAppStore()

const menuItems = [
  { path: "/dashboard", title: "Dashboard", icon: "Odometer" },
  { path: "/customers", title: "Customers", icon: "User" },
  { path: "/bidding", title: "Bidding", icon: "Document" },
  { path: "/projects", title: "Projects", icon: "List" },
  { path: "/relationships", title: "Relationships", icon: "Connection" },
  { path: "/contracts", title: "Contracts", icon: "Tickets" },
  { path: "/acceptance", title: "Acceptance", icon: "Checked" },
  { path: "/ltc", title: "LTC Pipeline", icon: "TrendCharts" },
  { path: "/ai-reports", title: "AI Reports", icon: "EditPen" },
  { path: "/knowledge", title: "Knowledge", icon: "Collection" },
  { path: "/settings", title: "Settings", icon: "Setting" },
]

const activeMenu = computed(() => route.path.startsWith("/customers") ? "/customers" : route.path)

function navigateTo(path: string) { router.push(path); if (appStore.isMobile) appStore.closeMobileMenu() }
</script>

<template>
  <div class="sidebar-container">
    <div class="sidebar-logo">
      <img :src="logoUrl" style="width:30px;height:30px;border-radius:6px" alt="HuiSmart" />
      <span v-show="!appStore.sidebarCollapsed || appStore.isMobile" class="logo-text">HuiSmart</span>
    </div>
    <el-menu :default-active="activeMenu" :collapse="appStore.sidebarCollapsed && !appStore.isMobile"
      background-color="#fbfbfd" text-color="#6e6e73" active-text-color="#0071e3" class="sidebar-menu">
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path" @click="navigateTo(item.path)">
        <el-icon><component :is="item.icon" /></el-icon>
        <template #title>{{ item.title }}</template>
      </el-menu-item>
    </el-menu>
    <div v-if="!appStore.isMobile" class="sidebar-collapse" @click="appStore.toggleSidebar()">
      <el-icon :size="16"><DArrowLeft v-if="!appStore.sidebarCollapsed" /><DArrowRight v-else /></el-icon>
    </div>
  </div>
</template>

<style scoped lang="scss">
.sidebar-container { display: flex; flex-direction: column; height: 100%; }
.sidebar-logo {
  height: 52px; display: flex; align-items: center; justify-content: center; gap: 10px;
  border-bottom: 1px solid rgba(0,0,0,0.04); flex-shrink: 0;
  .logo-text { color: #1d1d1f; font-size: 16px; font-weight: 700; white-space: nowrap; letter-spacing: -0.02em; }
}
.sidebar-menu {
  flex: 1; border-right: none; overflow-y: auto; overflow-x: hidden; padding: 6px 0;
  .el-menu-item {
    font-size: 13px; height: 38px; line-height: 38px;
    color: #6e6e73; margin: 1px 8px; border-radius: 8px;
    &:hover { background: rgba(0,0,0,0.04) !important; color: #1d1d1f !important; }
    &.is-active { background: rgba(0,113,227,0.08) !important; color: #0071e3 !important; font-weight: 600; }
  }
}
.sidebar-collapse {
  height: 34px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; color: #86868b; border-top: 1px solid rgba(0,0,0,0.04);
  transition: color 0.2s; flex-shrink: 0; &:hover { color: #1d1d1f; }
}
</style>""".encode())
print('Sidebar done')

sftp.close()

# Rebuild
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/202606AICRM/frontend && npx vite build --base=/aicrm/ 2>&1 | tail -5')
print('Build:', stdout.read().decode())
err = stderr.read().decode()
if err and 'error' in err.lower(): print('ERR:', err[:300])

client.close()
print('Done')
