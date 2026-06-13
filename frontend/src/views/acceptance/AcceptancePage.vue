<template>
  <div class="acceptance-page">
    <div class="page-header">
      <h2>验收管理</h2>
    </div>

    <el-tabs v-model="activeTab" type="border-card" class="acceptance-tabs">
      <!-- 待验收 -->
      <el-tab-pane label="待验收" name="pending">
        <el-table
          :data="pendingList"
          stripe
          border
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa', color: '#303133', fontWeight: 600 }"
          empty-text="暂无待验收项目"
        >
          <el-table-column prop="projectName" label="项目名称" min-width="180">
            <template #default="{ row }">
              <span class="project-name">{{ row.projectName }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="customer" label="客户" min-width="140" />
          <el-table-column prop="acceptanceDate" label="验收日期" width="130" sortable>
            <template #default="{ row }">
              <span>{{ row.acceptanceDate }}</span>
            </template>
          </el-table-column>
          <el-table-column label="验收标准" min-width="220">
            <template #default="{ row }">
              <el-tag
                v-for="criterion in row.criteria"
                :key="criterion"
                size="small"
                class="criteria-tag"
                type="info"
              >
                {{ criterion }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag type="warning" size="small">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" size="small" :icon="Check" @click="handleApprove(row)">
                发起验收
              </el-button>
              <el-button type="danger" size="small" :icon="Close" @click="handleReject(row)">
                驳回
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 已通过 -->
      <el-tab-pane label="已通过" name="approved">
        <el-table
          :data="approvedList"
          stripe
          border
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa', color: '#303133', fontWeight: 600 }"
          empty-text="暂无已通过项目"
        >
          <el-table-column prop="projectName" label="项目名称" min-width="180">
            <template #default="{ row }">
              <span class="project-name">{{ row.projectName }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="customer" label="客户" min-width="140" />
          <el-table-column prop="acceptanceDate" label="验收日期" width="130" sortable />
          <el-table-column label="验收标准" min-width="220">
            <template #default="{ row }">
              <el-tag
                v-for="criterion in row.criteria"
                :key="criterion"
                size="small"
                class="criteria-tag"
                type="success"
              >
                {{ criterion }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="110">
            <template #default="{ row }">
              <div class="approved-status">
                <el-icon class="check-icon"><CircleCheckFilled /></el-icon>
                <span class="status-text--success">{{ row.status }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="passedDate" label="通过日期" width="130" sortable>
            <template #default="{ row }">
              <span class="passed-date">{{ row.passedDate }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" size="small" link @click="handleViewDetail(row)">
                查看详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <!-- 已驳回 -->
      <el-tab-pane label="已驳回" name="rejected">
        <el-table
          :data="rejectedList"
          stripe
          border
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa', color: '#303133', fontWeight: 600 }"
          empty-text="暂无已驳回项目"
        >
          <el-table-column prop="projectName" label="项目名称" min-width="180">
            <template #default="{ row }">
              <span class="project-name">{{ row.projectName }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="customer" label="客户" min-width="140" />
          <el-table-column prop="acceptanceDate" label="验收日期" width="130" sortable />
          <el-table-column label="验收标准" min-width="220">
            <template #default="{ row }">
              <el-tag
                v-for="criterion in row.criteria"
                :key="criterion"
                size="small"
                class="criteria-tag"
                type="danger"
              >
                {{ criterion }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="110">
            <template #default="{ row }">
              <div class="rejected-status">
                <el-icon class="cross-icon"><CircleCloseFilled /></el-icon>
                <span class="status-text--danger">{{ row.status }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="驳回原因" min-width="180">
            <template #default="{ row }">
              <el-tooltip
                :content="row.rejectReason"
                placement="top"
                :show-after="300"
                effect="dark"
              >
                <span class="reject-reason-text">{{ row.rejectReason }}</span>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="140" fixed="right">
            <template #default="{ row }">
              <el-button type="warning" size="small" @click="handleResubmit(row)">
                重新提交
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Check, Close, CircleCheckFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

interface AcceptanceItem {
  id: number
  projectName: string
  customer: string
  acceptanceDate: string
  criteria: string[]
  status: string
  passedDate?: string
  rejectReason?: string
}

const activeTab = ref('pending')

const pendingList = reactive<AcceptanceItem[]>([
  {
    id: 1,
    projectName: '智慧城市数据中心平台',
    customer: '杭州市政府',
    acceptanceDate: '2026-06-18',
    criteria: ['功能完整性', '性能达标', '安全合规', '文档齐全'],
    status: '待验收',
  },
  {
    id: 2,
    projectName: '企业ERP升级项目',
    customer: '华远集团',
    acceptanceDate: '2026-06-22',
    criteria: ['数据迁移正确', '接口联调通过', '用户培训完成'],
    status: '待验收',
  },
  {
    id: 3,
    projectName: 'AI智能客服系统',
    customer: '平安保险',
    acceptanceDate: '2026-06-28',
    criteria: ['意图识别准确率', '响应时间达标', '知识库覆盖', '7x24稳定性'],
    status: '待验收',
  },
  {
    id: 4,
    projectName: '供应链管理平台',
    customer: '京东物流',
    acceptanceDate: '2026-07-05',
    criteria: ['库存同步准确', '订单流转正常', '报表数据一致', 'SLA达标'],
    status: '待验收',
  },
  {
    id: 5,
    projectName: '金融风控系统升级',
    customer: '工商银行',
    acceptanceDate: '2026-07-10',
    criteria: ['风控规则覆盖', '误报率低', '审计日志完整', '高可用架构'],
    status: '待验收',
  },
])

const approvedList = reactive<AcceptanceItem[]>([
  {
    id: 6,
    projectName: '政务一体化服务平台',
    customer: '浙江省政府',
    acceptanceDate: '2026-05-20',
    criteria: ['功能完整性', '安全合规', '性能达标', '文档齐全'],
    status: '已通过',
    passedDate: '2026-05-22',
  },
  {
    id: 7,
    projectName: 'CRM系统重构',
    customer: '中国移动',
    acceptanceDate: '2026-05-10',
    criteria: ['数据迁移正确', '接口联调通过', '用户验收签字'],
    status: '已通过',
    passedDate: '2026-05-12',
  },
  {
    id: 8,
    projectName: '物联网设备管理平台',
    customer: '海尔智家',
    acceptanceDate: '2026-04-25',
    criteria: ['设备接入正常', '数据上报准确', '告警机制有效'],
    status: '已通过',
    passedDate: '2026-04-28',
  },
  {
    id: 9,
    projectName: '医院HIS信息系统',
    customer: '瑞金医院',
    acceptanceDate: '2026-04-15',
    criteria: ['挂号流程正常', '电子病历合规', '医保对接成功', '等保三级'],
    status: '已通过',
    passedDate: '2026-04-18',
  },
])

const rejectedList = reactive<AcceptanceItem[]>([
  {
    id: 10,
    projectName: '大数据分析平台',
    customer: '招商银行',
    acceptanceDate: '2026-05-28',
    criteria: ['报表准确性', '查询性能', '数据一致性'],
    status: '已驳回',
    rejectReason: '报表模块数据与源系统存在5%偏差，需修复数据同步逻辑后重新提交验收',
  },
  {
    id: 11,
    projectName: '视频监控云平台',
    customer: '海康威视',
    acceptanceDate: '2026-05-15',
    criteria: ['视频流稳定性', '存储周期', '并发接入能力'],
    status: '已驳回',
    rejectReason: '并发接入测试未达标，当前仅支持500路并发，合同要求1000路以上',
  },
  {
    id: 12,
    projectName: '移动支付网关',
    customer: '拉卡拉',
    acceptanceDate: '2026-04-30',
    criteria: ['交易成功率', '响应延迟', '对账准确性', '容灾切换'],
    status: '已驳回',
    rejectReason: '容灾切换演练中主备切换耗时超30秒，不满足RTO<=10秒的要求',
  },
])

function handleApprove(row: AcceptanceItem) {
  ElMessageBox.confirm(
    `确认对项目"${row.projectName}"发起验收？`,
    '确认验收',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'success',
    }
  )
    .then(() => {
      const index = pendingList.findIndex((item) => item.id === row.id)
      if (index !== -1) {
        const [removed] = pendingList.splice(index, 1)
        approvedList.push({
          ...removed,
          status: '已通过',
          passedDate: new Date().toISOString().split('T')[0],
        })
      }
      ElMessage.success(`项目"${row.projectName}"验收已通过`)
    })
    .catch(() => {
      // Cancelled
    })
}

function handleReject(row: AcceptanceItem) {
  ElMessageBox.prompt(
    '请输入驳回原因',
    '驳回验收',
    {
      confirmButtonText: '确认驳回',
      cancelButtonText: '取消',
      type: 'warning',
      inputType: 'textarea',
      inputPlaceholder: '请详细描述驳回原因...',
      inputValidator: (value: string) => {
        if (!value || value.trim() === '') {
          return '驳回原因不能为空'
        }
        return true
      },
    }
  )
    .then(({ value }) => {
      const index = pendingList.findIndex((item) => item.id === row.id)
      if (index !== -1) {
        const [removed] = pendingList.splice(index, 1)
        rejectedList.push({
          ...removed,
          status: '已驳回',
          rejectReason: value.trim(),
        })
      }
      ElMessage.warning(`项目"${row.projectName}"已驳回`)
    })
    .catch(() => {
      // Cancelled
    })
}

function handleResubmit(row: AcceptanceItem) {
  ElMessageBox.confirm(
    `确定将项目"${row.projectName}"重新提交验收？`,
    '重新提交',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'info',
    }
  )
    .then(() => {
      const index = rejectedList.findIndex((item) => item.id === row.id)
      if (index !== -1) {
        const [removed] = rejectedList.splice(index, 1)
        const { rejectReason, ...rest } = removed
        pendingList.push({
          ...rest,
          status: '待验收',
        })
      }
      ElMessage.info(`项目"${row.projectName}"已重新提交验收`)
    })
    .catch(() => {
      // Cancelled
    })
}

function handleViewDetail(row: AcceptanceItem) {
  ElMessageBox.alert(
    `<div>
      <p><strong>项目名称：</strong>${row.projectName}</p>
      <p><strong>客户：</strong>${row.customer}</p>
      <p><strong>验收日期：</strong>${row.acceptanceDate}</p>
      <p><strong>通过日期：</strong>${row.passedDate}</p>
      <p><strong>验收标准：</strong>${row.criteria.join('、')}</p>
    </div>`,
    '验收详情',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '关闭',
      type: 'info',
    }
  )
}
</script>

<style scoped lang="scss">
.acceptance-page {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 22px;
      font-weight: 600;
      color: #303133;
    }
  }

  .acceptance-tabs {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);

    ::v-deep(.el-tabs__header) {
      background: #fafafa;
      margin-bottom: 0;
    }

    ::v-deep(.el-tabs__content) {
      padding: 16px;
    }
  }

  .project-name {
    font-weight: 600;
    color: #303133;
  }

  .criteria-tag {
    margin-right: 4px;
    margin-bottom: 4px;
  }

  .approved-status {
    display: flex;
    align-items: center;
    gap: 6px;

    .check-icon {
      font-size: 18px;
      color: #67c23a;
    }
  }

  .rejected-status {
    display: flex;
    align-items: center;
    gap: 6px;

    .cross-icon {
      font-size: 18px;
      color: #f56c6c;
    }
  }

  .status-text--success {
    color: #67c23a;
    font-weight: 500;
  }

  .status-text--danger {
    color: #f56c6c;
    font-weight: 500;
  }

  .passed-date {
    color: #67c23a;
    font-weight: 500;
  }

  .reject-reason-text {
    display: inline-block;
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #f56c6c;
    cursor: pointer;
    border-bottom: 1px dashed #f56c6c;

    &:hover {
      color: #e04040;
    }
  }
}
</style>
