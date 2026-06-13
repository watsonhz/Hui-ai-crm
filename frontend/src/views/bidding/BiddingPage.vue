<template>
  <div class="bidding-page">
    <div class="page-header">
      <h2>招投标管理</h2>
      <el-button type="primary" :icon="Plus">新建投标</el-button>
    </div>

    <div class="kanban-board">
      <el-row :gutter="12" class="kanban-row">
        <el-col
          v-for="state in states"
          :key="state.key"
          :span="Math.floor(24 / states.length)"
          :xs="24"
          :sm="12"
          :md="Math.floor(24 / states.length)"
          :lg="Math.floor(24 / states.length)"
        >
          <el-card
            :shadow="'hover'"
            class="kanban-column"
            :body-style="{ padding: '0' }"
          >
            <template #header>
              <div
                class="column-header"
                :style="{ backgroundColor: state.color }"
              >
                <span class="column-title">{{ state.label }}</span>
                <el-badge
                  :value="state.items.length"
                  class="column-badge"
                  type="info"
                />
              </div>
            </template>

            <div class="column-body">
              <div
                v-for="item in state.items"
                :key="item.id"
                class="bid-card"
                draggable="true"
              >
                <div class="bid-card__header">
                  <span class="bid-card__name">{{ item.projectName }}</span>
                  <el-tag size="small" :type="item.urgencyType">
                    {{ item.urgency }}
                  </el-tag>
                </div>
                <div class="bid-card__info">
                  <div class="bid-card__customer">
                    <el-icon><User /></el-icon>
                    <span>{{ item.customer }}</span>
                  </div>
                  <div class="bid-card__amount">
                    <el-icon><Money /></el-icon>
                    <span class="amount-value">{{ item.amount }}</span>
                  </div>
                </div>
                <div class="bid-card__footer">
                  <el-icon><Clock /></el-icon>
                  <span>截止：{{ item.deadline }}</span>
                </div>
                <div class="bid-card__drag-handle">
                  <el-icon><Rank /></el-icon>
                </div>
              </div>

              <div v-if="state.items.length === 0" class="column-empty">
                暂无投标项目
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { Plus, User, Money, Clock, Rank } from '@element-plus/icons-vue'

interface BidItem {
  id: number
  projectName: string
  customer: string
  amount: string
  deadline: string
  urgency: string
  urgencyType: 'danger' | 'warning' | 'info' | 'success' | ''
}

interface KanbanState {
  key: string
  label: string
  color: string
  items: BidItem[]
}

const states = reactive<KanbanState[]>([
  {
    key: 'clue',
    label: '线索',
    color: '#E8F4FD',
    items: [
      { id: 1, projectName: '智慧城市数据中心', customer: 'XX市政府', amount: '¥580万', deadline: '2026-08-15', urgency: '紧急', urgencyType: 'danger' },
      { id: 2, projectName: '企业ERP升级项目', customer: '华远集团', amount: '¥320万', deadline: '2026-09-01', urgency: '正常', urgencyType: '' },
      { id: 3, projectName: '智能安防系统', customer: '万科创智', amount: '¥210万', deadline: '2026-10-20', urgency: '待评估', urgencyType: 'info' },
    ],
  },
  {
    key: 'opportunity',
    label: '商机确认',
    color: '#E6F7E6',
    items: [
      { id: 4, projectName: '云计算平台建设', customer: '中兴通讯', amount: '¥890万', deadline: '2026-07-30', urgency: '紧急', urgencyType: 'danger' },
      { id: 5, projectName: '大数据分析平台', customer: '招商银行', amount: '¥650万', deadline: '2026-11-15', urgency: '正常', urgencyType: '' },
    ],
  },
  {
    key: 'solution',
    label: '方案设计',
    color: '#FFF3E0',
    items: [
      { id: 6, projectName: '物联网平台搭建', customer: '海尔智家', amount: '¥430万', deadline: '2026-08-25', urgency: '正常', urgencyType: '' },
      { id: 7, projectName: 'AI客服系统', customer: '平安保险', amount: '¥380万', deadline: '2026-09-30', urgency: '重要', urgencyType: 'warning' },
      { id: 8, projectName: '供应链管理平台', customer: '京东物流', amount: '¥720万', deadline: '2026-12-01', urgency: '正常', urgencyType: '' },
    ],
  },
  {
    key: 'bidding',
    label: '投标中',
    color: '#E3F2FD',
    items: [
      { id: 9, projectName: '智慧交通系统', customer: '深圳交通局', amount: '¥1500万', deadline: '2026-07-15', urgency: '紧急', urgencyType: 'danger' },
      { id: 10, projectName: '医院信息化升级', customer: '协和医院', amount: '¥960万', deadline: '2026-09-10', urgency: '重要', urgencyType: 'warning' },
    ],
  },
  {
    key: 'negotiation',
    label: '商务谈判',
    color: '#F3E5F5',
    items: [
      { id: 11, projectName: '金融风控系统', customer: '工商银行', amount: '¥1100万', deadline: '2026-08-05', urgency: '重要', urgencyType: 'warning' },
      { id: 12, projectName: '教育云平台', customer: '教育部', amount: '¥2000万', deadline: '2026-10-01', urgency: '正常', urgencyType: '' },
    ],
  },
  {
    key: 'won',
    label: '中标',
    color: '#E8F5E9',
    items: [
      { id: 13, projectName: '政务OA系统', customer: '浙江省政府', amount: '¥680万', deadline: '2026-06-30', urgency: '正常', urgencyType: '' },
      { id: 14, projectName: '移动支付平台', customer: '支付宝', amount: '¥3500万', deadline: '2026-12-31', urgency: '重要', urgencyType: 'warning' },
    ],
  },
  {
    key: 'lost',
    label: '丢标',
    color: '#FFEBEE',
    items: [
      { id: 15, projectName: '网络安全项目', customer: '华为技术', amount: '¥450万', deadline: '2026-05-20', urgency: '已结束', urgencyType: 'info' },
      { id: 16, projectName: '仓储管理系统', customer: '顺丰速运', amount: '¥290万', deadline: '2026-04-15', urgency: '已结束', urgencyType: 'info' },
    ],
  },
  {
    key: 'delivery',
    label: '项目交付',
    color: '#E0F2F1',
    items: [
      { id: 17, projectName: 'CRM系统升级', customer: '中国移动', amount: '¥520万', deadline: '2026-07-01', urgency: '正常', urgencyType: '' },
      { id: 18, projectName: '电商平台重构', customer: '苏宁易购', amount: '¥780万', deadline: '2026-09-30', urgency: '重要', urgencyType: 'warning' },
      { id: 19, projectName: '数据中台建设', customer: '字节跳动', amount: '¥1800万', deadline: '2026-11-15', urgency: '正常', urgencyType: '' },
    ],
  },
  {
    key: 'maintenance',
    label: '维保',
    color: '#FCE4EC',
    items: [
      { id: 20, projectName: 'OA系统维保', customer: '国家电网', amount: '¥120万/年', deadline: '2027-06-30', urgency: '续约中', urgencyType: 'warning' },
      { id: 21, projectName: 'ERP系统维保', customer: '中石油', amount: '¥200万/年', deadline: '2027-03-15', urgency: '正常', urgencyType: '' },
    ],
  },
])
</script>

<style scoped lang="scss">
.bidding-page {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 22px;
      font-weight: 600;
      color: #303133;
    }
  }

  .kanban-board {
    overflow-x: auto;
    padding-bottom: 8px;
  }

  .kanban-row {
    flex-wrap: nowrap;
    min-width: max-content;
  }

  .kanban-column {
    width: 100%;
    min-height: 400px;
    border-radius: 8px;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
  }

  .column-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-radius: 8px 8px 0 0;
    margin: -1px;

    .column-title {
      font-size: 14px;
      font-weight: 600;
      color: #303133;
    }

    .column-badge {
      ::v-deep(.el-badge__content) {
        font-size: 11px;
      }
    }
  }

  .column-body {
    padding: 12px;
    min-height: 200px;
  }

  .bid-card {
    background: #fff;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 10px;
    cursor: grab;
    transition: all 0.2s;
    position: relative;

    &:hover {
      border-color: #409eff;
      box-shadow: 0 2px 8px rgba(64, 158, 255, 0.15);
      transform: translateY(-1px);
    }

    &:active {
      cursor: grabbing;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    &__header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 8px;
    }

    &__name {
      font-size: 13px;
      font-weight: 600;
      color: #303133;
      line-height: 1.4;
      flex: 1;
      margin-right: 6px;
    }

    &__info {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 8px;
    }

    &__customer,
    &__amount {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: #606266;

      .el-icon {
        font-size: 13px;
        color: #909399;
        flex-shrink: 0;
      }
    }

    .amount-value {
      color: #e6a23c;
      font-weight: 500;
    }

    &__footer {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      color: #c0c4cc;
      padding-top: 8px;
      border-top: 1px dashed #ebeef5;
    }

    &__drag-handle {
      position: absolute;
      top: 8px;
      right: 8px;
      color: #c0c4cc;
      font-size: 14px;
      cursor: grab;
      opacity: 0;
      transition: opacity 0.2s;
    }

    &:hover &__drag-handle {
      opacity: 1;
    }
  }

  .column-empty {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 120px;
    color: #c0c4cc;
    font-size: 13px;
    border: 1px dashed #e4e7ed;
    border-radius: 4px;
  }
}
</style>
