<script setup lang="ts">
import { ref, computed } from 'vue'
import ContractTimeline from '@/components/visit/ContractTimeline.vue'

// ---- 合同列表 ----
const contracts = ref([
  { id: 1, name: 'IT运维平台年度服务合同', customer: '中科曙光', amount: 5800000, status: '执行中', signDate: '2025-12-01', endDate: '2026-12-01' },
  { id: 2, name: '智慧园区管理平台开发合同', customer: '上海张江集团', amount: 12600000, status: '审批中', signDate: '2026-03-15', endDate: '2027-03-15' },
  { id: 3, name: '大数据分析平台采购合同', customer: '浙江省大数据局', amount: 8600000, status: '已完成', signDate: '2024-06-01', endDate: '2025-12-31' },
  { id: 4, name: '云计算基础设施扩容合同', customer: '深圳华为', amount: 3200000, status: '执行中', signDate: '2026-01-10', endDate: '2026-09-30' },
])
const search = ref('')
const filtered = computed(() => contracts.value.filter(c => c.name.includes(search.value) || c.customer.includes(search.value)))

const statusColors: Record<string, string> = { '审批中': 'warning', '执行中': 'primary', '已完成': 'success', '已终止': 'danger' }

// ---- 合同详情 ----
const detailVisible = ref(false)
const selectedContract = ref<any>(null)
const deliveryStages = [
  { name: '合同签订', date: '', status: 'done' as const, desc: '' },
  { name: '项目启动', date: '', status: 'done' as const, desc: '' },
  { name: '需求分析', date: '', status: 'done' as const, desc: '' },
  { name: '设计开发', date: '', status: 'active' as const, desc: '当前阶段' },
  { name: '测试验收', date: '', status: 'pending' as const, desc: '' },
  { name: '上线部署', date: '', status: 'pending' as const, desc: '' },
  { name: '项目交付', date: '', status: 'pending' as const, desc: '' },
]
const payments = [
  { id: 1, planDate: '2025-12-15', planAmount: 1740000, actualDate: '2025-12-20', actualAmount: 1740000, ratio: '30%', status: 'done' },
  { id: 2, planDate: '2026-06-01', planAmount: 2320000, actualDate: '2026-06-05', actualAmount: 2320000, ratio: '40%', status: 'done' },
  { id: 3, planDate: '2026-12-01', planAmount: 1740000, actualDate: '', actualAmount: 0, ratio: '30%', status: 'pending' },
]

function showDetail(row: any) {
  selectedContract.value = row
  deliveryStages[0].date = row.signDate; deliveryStages[0].desc = `${row.amount.toLocaleString()} 元`
  deliveryStages[1].date = row.signDate
  deliveryStages[2].date = ''
  detailVisible.value = true
}
</script>

<template>
  <div class="contract-page">
    <div class="page-header">
      <h2>合同管理</h2>
      <el-button type="primary">+ 新建合同</el-button>
    </div>

    <!-- 列表 -->
    <el-card shadow="hover">
      <el-input v-model="search" placeholder="搜索合同名称/客户" clearable style="width:320px;margin-bottom:16px" />
      <el-table :data="filtered" stripe @row-click="showDetail" style="cursor:pointer">
        <el-table-column prop="name" label="合同名称" min-width="220" />
        <el-table-column prop="customer" label="客户" width="140" />
        <el-table-column prop="amount" label="金额" width="140" sortable>
          <template #default="{ row }">¥ {{ row.amount.toLocaleString() }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusColors[row.status]">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="signDate" label="签署日期" width="120" />
        <el-table-column prop="endDate" label="到期日" width="120" />
      </el-table>
    </el-card>

    <!-- 详情 Dialog -->
    <el-dialog v-model="detailVisible" :title="selectedContract?.name" width="800px" top="5vh">
      <template v-if="selectedContract">
        <el-descriptions :column="2" border size="small" style="margin-bottom:20px">
          <el-descriptions-item label="客户">{{ selectedContract.customer }}</el-descriptions-item>
          <el-descriptions-item label="金额">¥ {{ selectedContract.amount.toLocaleString() }}</el-descriptions-item>
          <el-descriptions-item label="签署日期">{{ selectedContract.signDate }}</el-descriptions-item>
          <el-descriptions-item label="到期日">{{ selectedContract.endDate }}</el-descriptions-item>
        </el-descriptions>

        <h4 class="section-title">📋 审批状态流</h4>
        <el-steps :active="selectedContract.status === '审批中' ? 1 : selectedContract.status === '执行中' ? 2 : 3" finish-status="success">
          <el-step title="合同起草" />
          <el-step title="法务审批" />
          <el-step title="签署盖章" />
          <el-step title="归档执行" />
        </el-steps>

        <h4 class="section-title">📦 交付阶段时间线</h4>
        <ContractTimeline :stages="deliveryStages" />

        <h4 class="section-title">💰 回款计划</h4>
        <el-table :data="payments" size="small">
          <el-table-column prop="ratio" label="比例" width="70" />
          <el-table-column prop="planAmount" label="计划金额" width="130">
            <template #default="{ row }">¥ {{ row.planAmount.toLocaleString() }}</template>
          </el-table-column>
          <el-table-column prop="planDate" label="计划日期" width="120" />
          <el-table-column prop="actualAmount" label="实收金额" width="130">
            <template #default="{ row }">{{ row.actualAmount ? '¥ ' + row.actualAmount.toLocaleString() : '-' }}</template>
          </el-table-column>
          <el-table-column prop="actualDate" label="实收日期" width="120">
            <template #default="{ row }">{{ row.actualDate || '-' }}</template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="90">
            <template #default="{ row }">
              <el-tag :type="row.status === 'done' ? 'success' : 'warning'" size="small">{{ row.status === 'done' ? '已回款' : '待回款' }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped lang="scss">
.contract-page { .page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; h2 { margin: 0; } } }
.section-title { margin: 20px 0 12px; font-size: 15px; }
</style>
