<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('customers')
const format = ref<'excel' | 'csv' | 'pdf'>('excel')
const dateRange = ref<[string, string]>(['', ''])
const exporting = ref(false)

const customerFields = ref([
  { key: 'name', label: '客户名称', selected: true },
  { key: 'company', label: '公司', selected: true },
  { key: 'phone', label: '电话', selected: true },
  { key: 'email', label: '邮箱', selected: true },
  { key: 'industry', label: '行业', selected: false },
  { key: 'level', label: '等级', selected: false },
  { key: 'status', label: '状态', selected: false },
  { key: 'source', label: '来源', selected: false },
])

function doExport() {
  exporting.value = true
  setTimeout(() => {
    exporting.value = false
    const ext = format.value === 'excel' ? 'xlsx' : format.value === 'pdf' ? 'pdf' : 'csv'
    ElMessage.success(`导出成功：${activeTab.value}_报告.${ext}（演示模式）`)
  }, 1500)
}
</script>

<template>
  <div class="export-page">
    <h2>数据导出</h2>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="客户导出" name="customers">
        <el-card shadow="hover">
          <h4>选择导出字段</h4>
          <el-checkbox-group>
            <el-checkbox v-for="f in customerFields" :key="f.key" v-model="f.selected">{{ f.label }}</el-checkbox>
          </el-checkbox-group>
        </el-card>
      </el-tab-pane>
      <el-tab-pane label="投标导出" name="bidding">
        <el-card shadow="hover"><p>投标数据导出为 CSV 格式，包含所有字段。</p></el-card>
      </el-tab-pane>
      <el-tab-pane label="报表导出" name="report">
        <el-card shadow="hover">
          <h4>选择日期范围</h4>
          <el-date-picker v-model="dateRange" type="daterange" range-separator="至" start-placeholder="开始" end-placeholder="结束" style="width:300px" />
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-card shadow="hover" style="margin-top:16px">
      <h4>导出格式</h4>
      <el-radio-group v-model="format">
        <el-radio value="excel">Excel (.xlsx)</el-radio>
        <el-radio value="csv">CSV (.csv)</el-radio>
        <el-radio value="pdf" :disabled="activeTab === 'bidding'">PDF (.pdf)</el-radio>
      </el-radio-group>
      <div style="margin-top:16px">
        <el-button type="primary" :loading="exporting" size="large" @click="doExport">
          {{ exporting ? '导出中...' : '开始导出' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>
