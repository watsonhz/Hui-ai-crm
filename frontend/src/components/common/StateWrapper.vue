<script setup lang="ts">
defineProps<{ loading?: boolean; error?: string | null; empty?: boolean; emptyText?: string }>()
const emit = defineEmits<{ retry: [] }>()
</script>

<template>
  <div class="state-wrapper">
    <div v-if="loading" class="state-content"><LoadingSkeleton /></div>
    <div v-else-if="error" class="state-content state-error">
      <el-result icon="error" :title="error" sub-title="请检查网络后重试">
        <template #extra><el-button type="primary" @click="emit('retry')">重试</el-button></template>
      </el-result>
    </div>
    <div v-else-if="empty" class="state-content state-empty">
      <el-empty :description="emptyText || '暂无数据'" />
    </div>
    <div v-else class="state-content">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.state-wrapper { min-height: 120px; }
.state-content { display: flex; align-items: center; justify-content: center; }
.state-error, .state-empty { padding: 40px 0; }
</style>
