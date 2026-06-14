<script setup lang="ts">
import { ref } from 'vue'
import type { UploadFile } from 'element-plus'

const files = ref<UploadFile[]>([])
const uploading = ref(false)

function handleChange(file: UploadFile) {
  files.value.push(file)
}

function handleRemove(file: UploadFile) {
  const idx = files.value.indexOf(file)
  if (idx > -1) files.value.splice(idx, 1)
}

function uploadAll() {
  uploading.value = true
  setTimeout(() => { uploading.value = false; files.value = [] }, 2000)
}

const isImage = (file: UploadFile) => file.raw?.type?.startsWith('image/')
const isPDF = (file: UploadFile) => file.raw?.type === 'application/pdf' || file.name?.endsWith('.pdf')
</script>

<template>
  <div class="file-upload">
    <el-upload drag multiple :auto-upload="false" :on-change="handleChange" :on-remove="handleRemove">
      <el-icon :size="40"><UploadFilled /></el-icon>
      <div>拖拽文件到此处或<em>点击上传</em></div>
      <template #tip>支持 PDF、Word、图片，单文件最大 50MB</template>
    </el-upload>

    <div v-if="files.length" class="file-list">
      <div v-for="f in files" :key="f.uid" class="file-item">
        <el-image v-if="isImage(f)" :src="f.url" fit="cover" style="width:48px;height:48px;border-radius:4px" />
        <el-icon v-else-if="isPDF(f)" :size="32" color="#F56C6C"><Document /></el-icon>
        <el-icon v-else :size="32" color="#409EFF"><Document /></el-icon>
        <span class="file-name">{{ f.name }}</span>
        <el-button size="small" text type="danger" @click="handleRemove(f)">删除</el-button>
      </div>
      <el-button type="primary" :loading="uploading" @click="uploadAll" style="margin-top:12px">
        {{ uploading ? '上传中...' : `上传 ${files.length} 个文件` }}
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.file-list { margin-top: 16px; }
.file-item { display: flex; align-items: center; gap: 12px; padding: 8px; border: 1px solid #eee; border-radius: 6px; margin-bottom: 8px; }
.file-name { flex: 1; font-size: 13px; }
</style>
