<script setup lang="ts">
defineProps<{ rows?: number; type?: 'card' | 'table' | 'chart' }>()
</script>

<template>
  <div class="skeleton-wrap">
    <!-- Card skeleton -->
    <template v-if="type === 'card' || !type">
      <div v-for="i in (rows || 4)" :key="i" class="sk-card">
        <div class="sk-line sk-title" />
        <div class="sk-line sk-text" />
        <div class="sk-line sk-text short" />
      </div>
    </template>
    <!-- Table skeleton -->
    <template v-if="type === 'table'">
      <div class="sk-table-header">
        <div v-for="i in 4" :key="i" class="sk-line sk-col" />
      </div>
      <div v-for="i in (rows || 5)" :key="i" class="sk-table-row">
        <div v-for="j in 4" :key="j" class="sk-line sk-cell" />
      </div>
    </template>
    <!-- Chart skeleton -->
    <template v-if="type === 'chart'">
      <div class="sk-chart" />
    </template>
  </div>
</template>

<style scoped lang="scss">
.skeleton-wrap { padding: 16px; }
.sk-line { height: 14px; background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 4px; margin-bottom: 10px; }
.sk-title { width: 50%; height: 20px; }
.sk-text { width: 90%; }
.sk-text.short { width: 60%; }
.sk-card { padding: 16px; background: #fff; border-radius: 8px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,.06); }
.sk-table-header, .sk-table-row { display: flex; gap: 12px; margin-bottom: 10px; }
.sk-col, .sk-cell { flex: 1; height: 32px; }
.sk-chart { height: 300px; @extend .sk-line; width: 100%; }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
</style>
