import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const currentPageTitle = ref('')

  const sidebarWidth = computed(() => (sidebarCollapsed.value ? '64px' : '220px'))

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setPageTitle(title: string) {
    currentPageTitle.value = title
    document.title = `${title} — AI CRM`
  }

  return {
    sidebarCollapsed,
    currentPageTitle,
    sidebarWidth,
    toggleSidebar,
    setPageTitle,
  }
})
