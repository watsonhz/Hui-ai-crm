<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, UploadFile } from 'element-plus'

const emit = defineEmits<{ submit: [data: any]; cancel: [] }>()
const formRef = ref<FormInstance>()
const uploading = ref(false)

const form = reactive({
  projectName: '', acceptanceStage: '', acceptanceDate: '',
  criteria: [] as string[], result: 'pass' as 'pass' | 'fail' | 'conditional',
  remarks: '', attachments: [] as UploadFile[],
})

const stages = ['初验', '终验', '阶段性验收']
const defaultCriteria: Record<string, string[]> = {
  '初验': ['功能完整性', '界面交互', '基础性能'],
  '终验': ['全部功能', '性能指标', '安全合规', '文档交付'],
  '阶段性验收': ['阶段目标达成', '交付物完整', '客户确认'],
}

function onStageChange(val: string) {
  form.criteria = [...(defaultCriteria[val] || [])]
}

function handleUpload(file: UploadFile) {
  form.attachments.push(file)
  return false
}

function submitForm() {
  if (!form.projectName || !form.acceptanceDate) {
    ElMessage.warning('请填写必填项')
    return
  }
  emit('submit', { ...form })
  ElMessage.success('验收提交成功')
}
</script>

<template>
  <el-form ref="formRef" :model="form" label-width="100px" @submit.prevent="submitForm">
    <el-form-item label="项目名称" required>
      <el-input v-model="form.projectName" placeholder="选择关联项目" />
    </el-form-item>
    <el-form-item label="验收阶段" required>
      <el-select v-model="form.acceptanceStage" @change="onStageChange">
        <el-option v-for="s in stages" :key="s" :label="s" :value="s" />
      </el-select>
    </el-form-item>
    <el-form-item label="验收日期" required>
      <el-date-picker v-model="form.acceptanceDate" type="date" value-format="YYYY-MM-DD" />
    </el-form-item>
    <el-form-item label="验收标准">
      <el-checkbox-group v-model="form.criteria">
        <el-checkbox v-for="c in form.criteria" :key="c" :label="c" :value="c" />
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="验收结果" required>
      <el-radio-group v-model="form.result">
        <el-radio value="pass">✅ 通过</el-radio>
        <el-radio value="conditional">⚠️ 有条件通过</el-radio>
        <el-radio value="fail">❌ 不通过</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="备注">
      <el-input v-model="form.remarks" type="textarea" :rows="3" />
    </el-form-item>
    <el-form-item label="上传报告">
      <el-upload :auto-upload="false" drag :on-change="handleUpload">
        <el-icon><UploadFilled /></el-icon>
        <div>拖拽或点击上传验收报告</div>
      </el-upload>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm" :loading="uploading">提交验收</el-button>
      <el-button @click="emit('cancel')">取消</el-button>
    </el-form-item>
  </el-form>
</template>
