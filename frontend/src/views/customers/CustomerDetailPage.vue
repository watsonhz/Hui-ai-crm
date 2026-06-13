<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'

// ---- Types ----
interface DecisionMaker {
  id: number
  name: string
  role: string
  roleLabel: string
  influence: 'high' | 'medium' | 'low'
  department: string
  phone: string
}

// ---- Route ----
const route = useRoute()
const router = useRouter()
const customerId = computed(() => Number(route.params.id))

// ---- Customer info ----
const customerInfo = reactive({
  name: '',
  industry: '',
  level: 'B' as 'A' | 'B' | 'C' | 'D',
  status: 'active' as 'active' | 'inactive',
  contact: '',
  phone: '',
  email: '',
  address: '',
  source: '',
  createTime: '',
  scale: '',
  annualRevenue: '',
  lastVisit: '',
  totalVisits: 0,
  totalOrders: 0,
  totalAmount: 0,
  notes: '',
})

const levelConfig: Record<string, { label: string; type: '' | 'success' | 'warning' | 'danger' }> = {
  A: { label: 'A级', type: 'danger' },
  B: { label: 'B级', type: 'warning' },
  C: { label: 'C级', type: 'success' },
  D: { label: 'D级', type: '' },
}

// ---- AI diagnostics ----
const churnRiskScore = ref(0)
const crossSellScore = ref(0)
const relationHealthScore = ref(0)

const churnFactors = ref<string[]>([])
const crossSellOpportunities = ref<string[]>([])

// ---- Decision makers ----
const decisionMakers = ref<DecisionMaker[]>([])

// ---- Computed helpers ----
const helpers = {
  levelTagType: () => levelConfig[customerInfo.level]?.type ?? '',
  levelLabel: () => levelConfig[customerInfo.level]?.label ?? customerInfo.level,
  statusLabel: () => (customerInfo.status === 'active' ? '活跃' : '非活跃'),
  statusType: () => (customerInfo.status === 'active' ? 'success' : 'info'),

  churnColor: () => {
    if (churnRiskScore.value >= 70) return '#F56C6C'
    if (churnRiskScore.value >= 40) return '#E6A23C'
    return '#67C23A'
  },
  churnLevel: () => {
    if (churnRiskScore.value >= 70) return '高危'
    if (churnRiskScore.value >= 40) return '中危'
    return '安全'
  },

  crossSellColor: () => {
    if (crossSellScore.value >= 70) return '#409EFF'
    if (crossSellScore.value >= 40) return '#E6A23C'
    return '#909399'
  },
  crossSellLevel: () => {
    if (crossSellScore.value >= 70) return '高机会'
    if (crossSellScore.value >= 40) return '有机会'
    return '暂无'
  },

  relationColor: () => {
    if (relationHealthScore.value >= 80) return '#67C23A'
    if (relationHealthScore.value >= 60) return '#E6A23C'
    return '#F56C6C'
  },
  relationLevel: () => {
    if (relationHealthScore.value >= 80) return '健康'
    if (relationHealthScore.value >= 60) return '一般'
    return '需改善'
  },

  influenceConfig: (influence: string) => {
    switch (influence) {
      case 'high': return { label: '高影响力', type: 'danger' as const }
      case 'medium': return { label: '中影响力', type: 'warning' as const }
      default: return { label: '低影响力', type: 'info' as const }
    }
  },
}

// ---- Data fetching ----
function fetchCustomerDetail() {
  // Simulate API — replace with real API in production
  Object.assign(customerInfo, {
    name: '张伟',
    industry: '政府/国企',
    level: 'B' as const,
    status: 'active' as const,
    contact: '张先生',
    phone: '13812345678',
    email: 'zhangwei@gov-example.cn',
    address: '上海市浦东新区张江高科技园区',
    source: '招标项目转化',
    createTime: '2025-11-15',
    scale: '1000-5000人',
    annualRevenue: '5亿-10亿',
    lastVisit: '2026-06-10',
    totalVisits: 24,
    totalOrders: 8,
    totalAmount: 15680000,
    notes: '该客户为2025年中标后转化的长期合作客户，目前在谈二期扩容项目。关系稳定，但近期竞争对手接触频繁，需加强高层互动。',
  })

  // AI diagnostics data
  churnRiskScore.value = 62
  churnFactors.value = [
    '近30天互动频次下降40%',
    '竞争对手最近拜访了决策链关键人',
    '上一期合同还有45天到期，尚未收到续约意向',
  ]
  crossSellScore.value = 78
  crossSellOpportunities.value = [
    '已采购A产品，B产品存在强互补需求',
    '客户的兄弟单位正在使用C产品，可推进集团统一采购',
    '三期扩容项目中可打包增值服务模块',
  ]
  relationHealthScore.value = 68

  // Decision chain
  decisionMakers.value = [
    {
      id: 1,
      name: '王处长',
      role: 'economic',
      roleLabel: '经济决策者',
      influence: 'high',
      department: '信息化处',
      phone: '13900001111',
    },
    {
      id: 2,
      name: '李工',
      role: 'technical',
      roleLabel: '技术决策者',
      influence: 'high',
      department: '技术部',
      phone: '13900002222',
    },
    {
      id: 3,
      name: '赵经理',
      role: 'user',
      roleLabel: '使用者',
      influence: 'medium',
      department: '业务部',
      phone: '13900003333',
    },
    {
      id: 4,
      name: '刘主任',
      role: 'coach',
      roleLabel: 'Coach',
      influence: 'low',
      department: '办公室',
      phone: '13900004444',
    },
  ]
}

// ---- Handlers ----
function goBack() {
  router.push({ name: 'Customers' })
}

onMounted(() => {
  fetchCustomerDetail()
})
</script>

<template>
  <div class="customer-detail">
    <!-- Back button -->
    <div class="detail-header-bar">
      <el-button :icon="ArrowLeft" @click="goBack">返回列表</el-button>
      <span class="detail-title">客户详情 #{{ customerId }}</span>
    </div>

    <!-- Customer info card -->
    <el-card shadow="never" class="info-card">
      <div class="info-card-content">
        <div class="info-left">
          <div class="customer-name-row">
            <h2 class="customer-name">{{ customerInfo.name }}</h2>
            <el-tag :type="helpers.levelTagType()" size="small">
              {{ helpers.levelLabel() }}
            </el-tag>
            <el-tag :type="helpers.statusType()" size="small">
              {{ helpers.statusLabel() }}
            </el-tag>
          </div>
          <div class="customer-meta">
            <span><el-icon><component is="Collection" /></el-icon> {{ customerInfo.industry }}</span>
            <span>{{ customerInfo.contact }}</span>
            <span>{{ customerInfo.phone }}</span>
          </div>
        </div>
        <div class="info-right">
          <el-tooltip content="编辑客户信息" placement="top">
            <el-button circle :icon="'Edit'" plain />
          </el-tooltip>
        </div>
      </div>
    </el-card>

    <!-- Tabs -->
    <el-card shadow="never" class="tabs-card">
      <el-tabs type="border-card">
        <!-- Tab 1: 基本信息 -->
        <el-tab-pane label="基本信息">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="客户名称" :span="2">
              {{ customerInfo.name }}
            </el-descriptions-item>
            <el-descriptions-item label="所属行业">
              {{ customerInfo.industry }}
            </el-descriptions-item>
            <el-descriptions-item label="客户等级">
              <el-tag :type="helpers.levelTagType()" size="small">
                {{ helpers.levelLabel() }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="联系人">
              {{ customerInfo.contact }}
            </el-descriptions-item>
            <el-descriptions-item label="联系电话">
              {{ customerInfo.phone }}
            </el-descriptions-item>
            <el-descriptions-item label="电子邮箱">
              {{ customerInfo.email }}
            </el-descriptions-item>
            <el-descriptions-item label="客户来源">
              {{ customerInfo.source }}
            </el-descriptions-item>
            <el-descriptions-item label="所在地区">
              {{ customerInfo.address }}
            </el-descriptions-item>
            <el-descriptions-item label="人员规模">
              {{ customerInfo.scale }}
            </el-descriptions-item>
            <el-descriptions-item label="年营收">
              {{ customerInfo.annualRevenue }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ customerInfo.createTime }}
            </el-descriptions-item>
            <el-descriptions-item label="最近拜访">
              {{ customerInfo.lastVisit }}
            </el-descriptions-item>
            <el-descriptions-item label="累计拜访">
              {{ customerInfo.totalVisits }} 次
            </el-descriptions-item>
            <el-descriptions-item label="累计订单">
              {{ customerInfo.totalOrders }} 单 / {{ (customerInfo.totalAmount / 10000).toFixed(0) }} 万元
            </el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">
              {{ customerInfo.notes }}
            </el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>

        <!-- Tab 2: AI 诊断面板 -->
        <el-tab-pane label="AI 诊断面板">
          <div class="ai-panel">
            <!-- 流失风险 -->
            <div class="ai-alert-card" style="border-left-color: #F56C6C">
              <div class="ai-alert-header">
                <h3>流失风险</h3>
                <span class="ai-score" :style="{ color: helpers.churnColor() }">
                  {{ churnRiskScore }}分 - {{ helpers.churnLevel() }}
                </span>
              </div>
              <el-progress
                :percentage="churnRiskScore"
                :color="helpers.churnColor()"
                :stroke-width="8"
              />
              <ul class="ai-factors">
                <li v-for="(factor, i) in churnFactors" :key="i">
                  <el-icon color="#F56C6C"><component is="WarningFilled" /></el-icon>
                  {{ factor }}
                </li>
              </ul>
            </div>

            <!-- 交叉销售机会 -->
            <div class="ai-alert-card" style="border-left-color: #409EFF">
              <div class="ai-alert-header">
                <h3>交叉销售机会</h3>
                <span class="ai-score" :style="{ color: helpers.crossSellColor() }">
                  {{ crossSellScore }}分 - {{ helpers.crossSellLevel() }}
                </span>
              </div>
              <el-progress
                :percentage="crossSellScore"
                :color="helpers.crossSellColor()"
                :stroke-width="8"
              />
              <ul class="ai-factors">
                <li v-for="(opp, i) in crossSellOpportunities" :key="i">
                  <el-icon color="#409EFF"><component is="Opportunity" /></el-icon>
                  {{ opp }}
                </li>
              </ul>
            </div>

            <!-- 关系健康度 -->
            <div class="ai-alert-card" style="border-left-color: #67C23A">
              <div class="ai-alert-header">
                <h3>关系健康度</h3>
                <span class="ai-score" :style="{ color: helpers.relationColor() }">
                  {{ relationHealthScore }}分 - {{ helpers.relationLevel() }}
                </span>
              </div>
              <el-progress
                :percentage="relationHealthScore"
                :color="helpers.relationColor()"
                :stroke-width="8"
              />
              <div class="health-advice">
                <p v-if="relationHealthScore >= 80">
                  客户关系处于健康状态，继续保持当前互动节奏。
                </p>
                <p v-else-if="relationHealthScore >= 60">
                  关系状态一般，建议增加拜访频次和商务活动。
                </p>
                <p v-else>
                  关系需重点改善，建议安排高层拜访或定制关怀活动。
                </p>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Tab 3: 决策链图谱 -->
        <el-tab-pane label="决策链图谱">
          <div class="decision-chain">
            <div
              v-for="(dm, index) in decisionMakers"
              :key="dm.id"
              class="chain-node"
            >
              <div class="node-connector" v-if="index > 0">
                <div class="connector-line" />
              </div>
              <el-card shadow="hover" class="node-card">
                <div class="node-header">
                  <span class="node-role">{{ dm.roleLabel }}</span>
                  <el-tag
                    :type="helpers.influenceConfig(dm.influence).type"
                    size="small"
                  >
                    {{ helpers.influenceConfig(dm.influence).label }}
                  </el-tag>
                </div>
                <div class="node-body">
                  <p class="node-name">{{ dm.name }}</p>
                  <p class="node-dept">{{ dm.department }}</p>
                  <p class="node-phone">{{ dm.phone }}</p>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<style scoped lang="scss">
.customer-detail {
  padding: 16px;
}

.detail-header-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;

  .detail-title {
    font-size: 16px;
    color: #909399;
  }
}

// ---- Info card ----
.info-card {
  margin-bottom: 16px;
}

.info-card-content {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.info-left {
  .customer-name-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;

    .customer-name {
      font-size: 22px;
      font-weight: 700;
      color: #303133;
      margin: 0;
    }
  }

  .customer-meta {
    display: flex;
    gap: 20px;
    font-size: 13px;
    color: #606266;

    span {
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }
  }
}

// ---- Tabs ----
.tabs-card {
  :deep(.el-tabs__content) {
    padding: 20px;
  }
}

// ---- AI Panel ----
.ai-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ai-alert-card {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-left: 4px solid;
  border-radius: 6px;
  padding: 20px 24px;

  .ai-alert-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;

    h3 {
      margin: 0;
      font-size: 15px;
      font-weight: 600;
      color: #303133;
    }

    .ai-score {
      font-size: 18px;
      font-weight: 700;
    }
  }

  .ai-factors {
    margin: 12px 0 0;
    padding: 0;
    list-style: none;

    li {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 0;
      font-size: 13px;
      color: #606266;
      border-bottom: 1px dashed #ebeef5;

      &:last-child {
        border-bottom: none;
      }
    }
  }

  .health-advice {
    margin-top: 12px;
    padding: 10px 12px;
    background: #f5f7fa;
    border-radius: 4px;

    p {
      margin: 0;
      font-size: 13px;
      color: #606266;
      line-height: 1.6;
    }
  }
}

// ---- Decision Chain ----
.decision-chain {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 8px 0;
}

.chain-node {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.node-connector {
  display: flex;
  justify-content: center;
  padding: 4px 0;

  .connector-line {
    width: 2px;
    height: 32px;
    background: linear-gradient(to bottom, #c0c4cc, #dcdfe6);
    border-radius: 1px;
  }
}

.node-card {
  width: 100%;
  max-width: 480px;

  .node-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;

    .node-role {
      font-size: 14px;
      font-weight: 600;
      color: #303133;
    }
  }

  .node-body {
    .node-name {
      font-size: 15px;
      font-weight: 500;
      color: #303133;
      margin: 0 0 6px;
    }

    .node-dept,
    .node-phone {
      font-size: 12px;
      color: #909399;
      margin: 0 0 4px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}
</style>
