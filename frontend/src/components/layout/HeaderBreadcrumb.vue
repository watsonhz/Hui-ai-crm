<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { watch } from 'vue'
import NotificationCenter from '@/components/common/NotificationCenter.vue'

const route = useRoute()
const appStore = useAppStore()

// 面包屑自动生�?const breadcrumbs = computed(() => {
  const matched = route.matched.filter((r) => r.meta?.title)
  return matched.map((r) => ({
    title: r.meta?.title as string,
    path: r.path,
  }))
})

// 更新页面标题
watch(
  () => route.meta?.title,
  (title) => {
    if (title) appStore.setPageTitle(title as string)
  },
  { immediate: true },
)
</script>

<template>
  <div class="header-container">
    <!-- 左侧：面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path">
        {{ item.title }}
      </el-breadcrumb-item>
    </el-breadcrumb>

    <!-- 右侧：用户信�?-->
    <div class="header-right">
      <el-badge>\r\n        <NotificationCenter />\r\n        <el-icon :size="20"><Bell /></el-icon>
      </el-badge>
      <el-dropdown>
        <span class="user-info">
          <el-avatar :size="32" icon="UserFilled" />
          <span class="username">管理�?/span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>个人设置</el-dropdown-item>
            <el-dropdown-item divided>退出登�?/el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<style scoped lang="scss">
.header-container {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;

  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    .username {
      font-size: 14px;
      color: #333;
    }
  }
}
</style>
