<script setup lang="ts">
defineProps<{ stages: Array<{ name: string; date: string; status: 'done' | 'active' | 'pending'; desc: string }> }>()
</script>

<template>
  <el-timeline>
    <el-timeline-item
      v-for="s in stages" :key="s.name"
      :timestamp="s.date" placement="top"
      :color="s.status === 'done' ? '#67C23A' : s.status === 'active' ? '#409EFF' : '#909399'"
      :type="s.status === 'done' ? 'success' : s.status === 'active' ? 'primary' : 'info'"
    >
      <strong>{{ s.name }}</strong>
      <p class="stage-desc">{{ s.desc }}</p>
    </el-timeline-item>
  </el-timeline>
</template>

<style scoped>
.stage-desc { margin: 4px 0 0; font-size: 13px; color: #606266; }
</style>
