<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Search, User, DataLine, Coin,
} from '@element-plus/icons-vue'

// ---- Types ----
interface Customer {
  id: number
  name: string
  industry: string
  contact: string
  phone: string
  level: 'A' | 'B' | 'C' | 'D'
  status: 'active' | 'inactive'
  lastVisit: string
}

interface OrgNode {
  id: string
  label: string
  children?: OrgNode[]
}

// ---- Router ----
const router = useRouter()

// ---- Search filters ----
const filters = reactive({
  name: '',
  phone: '',
  industry: '',
})

const industryOptions = [
  { label: '政府/国企', value: '政府/国企' },
  { label: '制造业', value: '制造业' },
  { label: 'IT/互联网', value: 'IT/互联网' },
  { label: '金融', value: '金融' },
  { label: '医疗', value: '医疗' },
  { label: '教育', value: '教育' },
  { label: '房地产', value: '房地产' },
  { label: '能源', value: '能源' },
]

// ---- Stats ----
const stats = ref([
  { label: '客户总数', value: 0, icon: User, color: '#409EFF' },
  { label: '活跃客户', value: 0, icon: DataLine, color: '#67C23A' },
  { label: '本月新增', value: 0, icon: Coin, color: '#E6A23C' },
])

// ---- Table data ----
const tableData = ref<Customer[]>([])
const total = ref(0)
const pageSize = ref(10)
const currentPage = ref(1)
const tableLoading = ref(false)

// ---- Organization tree ----
const orgTreeData = ref<OrgNode[]>([
  {
    id: 'east',
    label: '华东区',
    children: [
      { id: 'shanghai', label: '上海' },
      { id: 'hangzhou', label: '杭州' },
    ],
  },
  {
    id: 'south',
    label: '华南区',
    children: [
      { id: 'shenzhen', label: '深圳' },
      { id: 'guangzhou', label: '广州' },
    ],
  },
])

const defaultExpandedKeys = ref(['east', 'south'])
const activeOrg = ref('')

// ---- Level mapping ----
const levelConfig: Record<string, { label: string; type: '' | 'success' | 'warning' | 'danger' }> = {
  A: { label: 'A', type: 'danger' },
  B: { label: 'B', type: 'warning' },
  C: { label: 'C', type: 'success' },
  D: { label: 'D', type: '' },
}

const levelOptions = computed(() =>
  Object.entries(levelConfig).map(([value, { label }]) => ({ label, value }))
)

// ---- Mock data generator ----
function generateMockData(): Customer[] {
  const industries = industryOptions.map((i) => i.value)
  const levels: Customer['level'][] = ['A', 'B', 'C', 'D']
  const statuses: Customer['status'][] = ['active', 'inactive']
  const surnames = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴']
  const names = ['伟', '芳', '娜', '敏', '静', '强', '磊', '洋', '勇', '军']

  return Array.from({ length: 46 }, (_, i) => ({
    id: i + 1,
    name: `${surnames[i % surnames.length]}${names[i % names.length]}`,
    industry: industries[i % industries.length],
    contact: `${surnames[(i + 3) % surnames.length]}主任`,
    phone: `138${String(10000000 + i).slice(0, 8)}`,
    level: levels[i % levels.length],
    status: statuses[i % 2],
    lastVisit: `2026-0${(i % 6) + 1}-${String((i % 28) + 1).padStart(2, '0')}`,
  }))
}

// ---- Data fetching ----
async function fetchData() {
  tableLoading.value = true
  // Simulate API call — replace with real API in production
  await new Promise((resolve) => setTimeout(resolve, 400))
  const allData = generateMockData()

  // Apply filters
  let filtered = allData
  if (filters.name) {
    filtered = filtered.filter((c) => c.name.includes(filters.name))
  }
  if (filters.phone) {
    filtered = filtered.filter((c) => c.phone.includes(filters.phone))
  }
  if (filters.industry) {
    filtered = filtered.filter((c) => c.industry === filters.industry)
  }

  total.value = filtered.length

  // Paginate
  const start = (currentPage.value - 1) * pageSize.value
  tableData.value = filtered.slice(start, start + pageSize.value)

  // Update stats
  stats.value = [
    { ...stats.value[0], value: allData.length },
    { ...stats.value[1], value: allData.filter((c) => c.status === 'active').length },
    { ...stats.value[2], value: 12 },
  ]

  tableLoading.value = false
}

// ---- Handlers ----
function handleSearch() {
  currentPage.value = 1
  fetchData()
}

function handleReset() {
  filters.name = ''
  filters.phone = ''
  filters.industry = ''
  currentPage.value = 1
  fetchData()
}

function handleSizeChange(val: number) {
  pageSize.value = val
  fetchData()
}

function handlePageChange(val: number) {
  currentPage.value = val
  fetchData()
}

function handleViewDetail(row: Customer) {
  router.push({ name: 'CustomerDetail', params: { id: row.id } })
}

function handleCreate() {
  ElMessage.info('新增客户功能（待实现）')
}

function handleOrgNodeClick(data: OrgNode) {
  activeOrg.value = data.id
  // In production, filter by org node
  fetchData()
}

function getLevelType(level: string) {
  return levelConfig[level]?.type ?? ''
}

function getLevelLabel(level: string) {
  return levelConfig[level]?.label ?? level
}

function getStatusLabel(status: string) {
  return status === 'active' ? '活跃' : '非活跃'
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="customer-list">
    <!-- Page header -->
    <div class="page-header">
      <h2 class="page-title">客户列表</h2>
      <el-button type="primary" :icon="Search" @click="handleCreate">
        新增客户
      </el-button>
    </div>

    <!-- Stats row -->
    <el-row :gutter="16" class="stats-row">
      <el-col v-for="s in stats" :key="s.label" :xs="8" :sm="8" :md="8" :lg="8">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-content">
            <div>
              <p class="stat-label">{{ s.label }}</p>
              <p class="stat-value" :style="{ color: s.color }">{{ s.value }}</p>
            </div>
            <div class="stat-icon" :style="{ background: s.color }">
              <el-icon :size="22" color="#fff">
                <component :is="s.icon" />
              </el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Main content: sidebar tree + table -->
    <div class="main-layout">
      <!-- Left sidebar: organization tree -->
      <aside class="org-sidebar">
        <el-card shadow="never" class="org-card">
          <template #header>
            <span class="org-card-title">组织架构</span>
          </template>
          <el-tree
            :data="orgTreeData"
            :default-expanded-keys="defaultExpandedKeys"
            node-key="id"
            highlight-current
            :expand-on-click-node="false"
            @node-click="handleOrgNodeClick"
          />
        </el-card>
      </aside>

      <!-- Right: search + table -->
      <div class="content-area">
        <!-- Search bar -->
        <el-card shadow="never" class="search-card">
          <el-form :model="filters" inline>
            <el-form-item label="客户名称">
              <el-input
                v-model="filters.name"
                placeholder="请输入客户名称"
                clearable
                style="width: 200px"
              />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input
                v-model="filters.phone"
                placeholder="请输入联系电话"
                clearable
                style="width: 200px"
              />
            </el-form-item>
            <el-form-item label="所属行业">
              <el-select
                v-model="filters.industry"
                placeholder="请选择行业"
                clearable
                style="width: 180px"
              >
                <el-option
                  v-for="opt in industryOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :icon="Search" @click="handleSearch">
                搜索
              </el-button>
              <el-button @click="handleReset">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- Table -->
        <el-card shadow="never" class="table-card">
          <el-table
            v-loading="tableLoading"
            :data="tableData"
            stripe
            style="width: 100%"
            :header-cell-style="{ background: '#f5f7fa', color: '#303133', fontWeight: 600 }"
          >
            <el-table-column prop="name" label="客户名称" min-width="140" />
            <el-table-column prop="industry" label="所属行业" min-width="120" />
            <el-table-column prop="contact" label="联系人" min-width="100" />
            <el-table-column prop="phone" label="联系电话" min-width="140" />
            <el-table-column label="客户等级" width="100" align="center">
              <template #default="{ row }">
                <el-tag
                  :type="getLevelType(row.level)"
                  size="small"
                >
                  {{ getLevelLabel(row.level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100" align="center">
              <template #default="{ row }">
                <el-tag
                  :type="row.status === 'active' ? 'success' : 'info'"
                  size="small"
                >
                  {{ getStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="lastVisit" label="最近拜访" width="130" />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="handleViewDetail(row)">
                  查看详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- Pagination -->
          <div class="pagination-wrap">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              background
              @size-change="handleSizeChange"
              @current-change="handlePageChange"
            />
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.customer-list {
  padding: 16px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;

  .page-title {
    font-size: 20px;
    font-weight: 600;
    color: #303133;
    margin: 0;
  }
}

.stats-row {
  margin-bottom: 16px;
}

.stat-card {
  .stat-content {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .stat-label {
      font-size: 13px;
      color: #909399;
      margin-bottom: 6px;
    }

    .stat-value {
      font-size: 28px;
      font-weight: 700;
      margin: 0;
    }

    .stat-icon {
      width: 48px;
      height: 48px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}

.main-layout {
  display: flex;
  gap: 16px;
}

.org-sidebar {
  width: 220px;
  flex-shrink: 0;
}

.org-card {
  height: 100%;

  .org-card-title {
    font-size: 14px;
    font-weight: 600;
  }
}

.content-area {
  flex: 1;
  min-width: 0;
}

.search-card {
  margin-bottom: 16px;
}

.table-card {
  .pagination-wrap {
    display: flex;
    justify-content: flex-end;
    margin-top: 16px;
  }
}
</style>
