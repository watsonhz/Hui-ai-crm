<template>
  <div class="projects-page">
    <div class="page-header">
      <h2>项目管理</h2>
      <el-button type="primary" :icon="Plus">新建项目</el-button>
    </div>

    <!-- Section: 售前阶段 -->
    <div class="stage-section">
      <div class="section-header">
        <span class="section-dot" style="background: #409eff"></span>
        <span class="section-title">售前阶段</span>
        <span class="section-count">{{ preSalesTotal }} 个项目</span>
      </div>
      <div class="kanban-board">
        <el-row :gutter="12" class="kanban-row">
          <el-col
            v-for="stage in preSalesStages"
            :key="stage.key"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-card
              :shadow="'hover'"
              class="kanban-column"
              :body-style="{ padding: '0' }"
            >
              <template #header>
                <div
                  class="column-header"
                  :style="{ backgroundColor: stage.color }"
                >
                  <span class="column-title">{{ stage.label }}</span>
                  <el-badge
                    :value="stage.items.length"
                    class="column-badge"
                    type="primary"
                  />
                </div>
              </template>

              <div
                class="column-body"
                @dragover.prevent="onDragOver"
                @drop.prevent="onDrop($event, stage.key)"
              >
                <div
                  v-for="item in stage.items"
                  :key="item.id"
                  class="project-card"
                  draggable="true"
                  @dragstart="onDragStart($event, item, stage.key)"
                >
                  <div class="project-card__header">
                    <span class="project-card__name">{{ item.projectName }}</span>
                    <el-tag :type="item.priorityType" size="small">
                      {{ item.priority }}
                    </el-tag>
                  </div>

                  <div class="project-card__info">
                    <div class="info-row">
                      <el-icon><OfficeBuilding /></el-icon>
                      <span>{{ item.customer }}</span>
                    </div>
                    <div class="info-row">
                      <el-icon><UserFilled /></el-icon>
                      <span>{{ item.pm }}</span>
                    </div>
                  </div>

                  <div class="project-card__progress">
                    <div class="progress-label">
                      <span>进度</span>
                      <span class="progress-value">{{ item.progress }}%</span>
                    </div>
                    <el-progress
                      :percentage="item.progress"
                      :stroke-width="6"
                      :color="getProgressColor(item.progress)"
                      :show-text="false"
                    />
                  </div>

                  <div class="project-card__drag-handle">
                    <el-icon><Rank /></el-icon>
                  </div>
                </div>

                <div v-if="stage.items.length === 0" class="column-empty">
                  暂无项目
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- Section: 合同阶段 -->
    <div class="stage-section">
      <div class="section-header">
        <span class="section-dot" style="background: #e6a23c"></span>
        <span class="section-title">合同阶段</span>
        <span class="section-count">{{ contractTotal }} 个项目</span>
      </div>
      <div class="kanban-board">
        <el-row :gutter="12" class="kanban-row">
          <el-col
            v-for="stage in contractStages"
            :key="stage.key"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-card
              :shadow="'hover'"
              class="kanban-column"
              :body-style="{ padding: '0' }"
            >
              <template #header>
                <div
                  class="column-header"
                  :style="{ backgroundColor: stage.color }"
                >
                  <span class="column-title">{{ stage.label }}</span>
                  <el-badge
                    :value="stage.items.length"
                    class="column-badge"
                    type="warning"
                  />
                </div>
              </template>

              <div
                class="column-body"
                @dragover.prevent="onDragOver"
                @drop.prevent="onDrop($event, stage.key)"
              >
                <div
                  v-for="item in stage.items"
                  :key="item.id"
                  class="project-card"
                  draggable="true"
                  @dragstart="onDragStart($event, item, stage.key)"
                >
                  <div class="project-card__header">
                    <span class="project-card__name">{{ item.projectName }}</span>
                    <el-tag :type="item.priorityType" size="small">
                      {{ item.priority }}
                    </el-tag>
                  </div>

                  <div class="project-card__info">
                    <div class="info-row">
                      <el-icon><OfficeBuilding /></el-icon>
                      <span>{{ item.customer }}</span>
                    </div>
                    <div class="info-row">
                      <el-icon><UserFilled /></el-icon>
                      <span>{{ item.pm }}</span>
                    </div>
                  </div>

                  <div class="project-card__progress">
                    <div class="progress-label">
                      <span>进度</span>
                      <span class="progress-value">{{ item.progress }}%</span>
                    </div>
                    <el-progress
                      :percentage="item.progress"
                      :stroke-width="6"
                      :color="getProgressColor(item.progress)"
                      :show-text="false"
                    />
                  </div>

                  <div class="project-card__drag-handle">
                    <el-icon><Rank /></el-icon>
                  </div>
                </div>

                <div v-if="stage.items.length === 0" class="column-empty">
                  暂无项目
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- Section: 交付阶段 -->
    <div class="stage-section">
      <div class="section-header">
        <span class="section-dot" style="background: #67c23a"></span>
        <span class="section-title">交付阶段</span>
        <span class="section-count">{{ deliveryTotal }} 个项目</span>
      </div>
      <div class="kanban-board">
        <el-row :gutter="12" class="kanban-row">
          <el-col
            v-for="stage in deliveryStages"
            :key="stage.key"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-card
              :shadow="'hover'"
              class="kanban-column"
              :body-style="{ padding: '0' }"
            >
              <template #header>
                <div
                  class="column-header"
                  :style="{ backgroundColor: stage.color }"
                >
                  <span class="column-title">{{ stage.label }}</span>
                  <el-badge
                    :value="stage.items.length"
                    class="column-badge"
                    type="success"
                  />
                </div>
              </template>

              <div
                class="column-body"
                @dragover.prevent="onDragOver"
                @drop.prevent="onDrop($event, stage.key)"
              >
                <div
                  v-for="item in stage.items"
                  :key="item.id"
                  class="project-card"
                  draggable="true"
                  @dragstart="onDragStart($event, item, stage.key)"
                >
                  <div class="project-card__header">
                    <span class="project-card__name">{{ item.projectName }}</span>
                    <el-tag :type="item.priorityType" size="small">
                      {{ item.priority }}
                    </el-tag>
                  </div>

                  <div class="project-card__info">
                    <div class="info-row">
                      <el-icon><OfficeBuilding /></el-icon>
                      <span>{{ item.customer }}</span>
                    </div>
                    <div class="info-row">
                      <el-icon><UserFilled /></el-icon>
                      <span>{{ item.pm }}</span>
                    </div>
                  </div>

                  <div class="project-card__progress">
                    <div class="progress-label">
                      <span>进度</span>
                      <span class="progress-value">{{ item.progress }}%</span>
                    </div>
                    <el-progress
                      :percentage="item.progress"
                      :stroke-width="6"
                      :color="getProgressColor(item.progress)"
                      :show-text="false"
                    />
                  </div>

                  <div class="project-card__drag-handle">
                    <el-icon><Rank /></el-icon>
                  </div>
                </div>

                <div v-if="stage.items.length === 0" class="column-empty">
                  暂无项目
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { Plus, OfficeBuilding, UserFilled, Rank } from '@element-plus/icons-vue'

interface ProjectItem {
  id: number
  projectName: string
  customer: string
  pm: string
  progress: number
  priority: string
  priorityType: 'danger' | 'warning' | 'info' | 'success' | ''
}

interface KanbanStage {
  key: string
  label: string
  color: string
  items: ProjectItem[]
}

const preSalesStages = reactive<KanbanStage[]>([
  {
    key: 'initial_contact',
    label: '初步接洽',
    color: '#E8F4FD',
    items: [
      { id: 1, projectName: '智慧城市大脑平台', customer: '杭州市政府', pm: '张伟', progress: 15, priority: '高', priorityType: 'danger' },
      { id: 2, projectName: '企业数字化转型', customer: '三一重工', pm: '李娜', progress: 8, priority: '中', priorityType: 'warning' },
      { id: 3, projectName: '智能客服系统调研', customer: '招商银行', pm: '王磊', progress: 5, priority: '低', priorityType: 'info' },
    ],
  },
  {
    key: 'requirement_analysis',
    label: '需求分析',
    color: '#E6F7E6',
    items: [
      { id: 4, projectName: '数据中台二期', customer: '字节跳动', pm: '赵敏', progress: 28, priority: '高', priorityType: 'danger' },
      { id: 5, projectName: '工业互联网平台', customer: '富士康', pm: '刘洋', progress: 22, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'demo',
    label: '方案演示',
    color: '#FFF3E0',
    items: [
      { id: 6, projectName: 'AI质检系统', customer: '比亚迪', pm: '陈静', progress: 38, priority: '高', priorityType: 'danger' },
      { id: 7, projectName: '零售中台方案', customer: '永辉超市', pm: '孙强', progress: 32, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'quotation',
    label: '报价',
    color: '#F3E5F5',
    items: [
      { id: 8, projectName: '云安全防护', customer: '中信证券', pm: '周明', progress: 48, priority: '高', priorityType: 'danger' },
      { id: 9, projectName: '物联网管理平台', customer: '美的集团', pm: '吴丽', progress: 42, priority: '中', priorityType: 'warning' },
    ],
  },
])

const contractStages = reactive<KanbanStage[]>([
  {
    key: 'negotiation',
    label: '商务谈判',
    color: '#E3F2FD',
    items: [
      { id: 10, projectName: '智慧交通调度', customer: '广州交通局', pm: '郑凯', progress: 55, priority: '高', priorityType: 'danger' },
      { id: 11, projectName: '金融风控系统', customer: '平安银行', pm: '冯丽', progress: 52, priority: '高', priorityType: 'danger' },
      { id: 12, projectName: '电商平台升级', customer: '唯品会', pm: '何伟', progress: 50, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'contract',
    label: '合同签订',
    color: '#FFF8E1',
    items: [
      { id: 13, projectName: '供应链协同平台', customer: '京东物流', pm: '林婷', progress: 65, priority: '高', priorityType: 'danger' },
      { id: 14, projectName: 'HR SaaS系统', customer: '万科集团', pm: '杨磊', progress: 60, priority: '中', priorityType: 'warning' },
    ],
  },
])

const deliveryStages = reactive<KanbanStage[]>([
  {
    key: 'kickoff',
    label: '项目启动',
    color: '#E8F5E9',
    items: [
      { id: 15, projectName: '政务一体化平台', customer: '浙江省政府', pm: '黄伟', progress: 72, priority: '高', priorityType: 'danger' },
      { id: 16, projectName: '医院HIS系统', customer: '瑞金医院', pm: '许静', progress: 68, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'design_dev',
    label: '设计开发',
    color: '#E0F2F1',
    items: [
      { id: 17, projectName: '智能制造MES', customer: '格力电器', pm: '曹阳', progress: 42, priority: '高', priorityType: 'danger' },
      { id: 18, projectName: '车联网平台', customer: '蔚来汽车', pm: '邓超', progress: 35, priority: '高', priorityType: 'danger' },
      { id: 19, projectName: '内容管理CMS', customer: '新华社', pm: '彭丽', progress: 28, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'testing',
    label: '测试验收',
    color: '#FFF3E0',
    items: [
      { id: 20, projectName: 'CRM系统重构', customer: '中国移动', pm: '田磊', progress: 82, priority: '高', priorityType: 'danger' },
      { id: 21, projectName: '数据仓库建设', customer: '银联', pm: '蒋敏', progress: 78, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'deploy',
    label: '上线部署',
    color: '#FCE4EC',
    items: [
      { id: 22, projectName: 'OA协同办公', customer: '国家电网', pm: '沈强', progress: 92, priority: '高', priorityType: 'danger' },
    ],
  },
  {
    key: 'delivery',
    label: '项目交付',
    color: '#E8F5E9',
    items: [
      { id: 23, projectName: '支付网关系统', customer: '拉卡拉', pm: '韩雪', progress: 98, priority: '高', priorityType: 'danger' },
      { id: 24, projectName: '视频监控云平台', customer: '海康威视', pm: '唐明', progress: 95, priority: '中', priorityType: 'warning' },
    ],
  },
  {
    key: 'maintenance',
    label: '维保服务',
    color: '#E3F2FD',
    items: [
      { id: 25, projectName: 'ERP系统维保', customer: '中石化', pm: '蔡琳', progress: 100, priority: '低', priorityType: 'info' },
      { id: 26, projectName: 'BI报表平台维保', customer: '中国电信', pm: '潘伟', progress: 100, priority: '低', priorityType: 'info' },
      { id: 27, projectName: '客服系统维保', customer: '顺丰速运', pm: '龚丽', progress: 100, priority: '低', priorityType: 'info' },
    ],
  },
])

const preSalesTotal = computed(() =>
  preSalesStages.reduce((sum, s) => sum + s.items.length, 0)
)
const contractTotal = computed(() =>
  contractStages.reduce((sum, s) => sum + s.items.length, 0)
)
const deliveryTotal = computed(() =>
  deliveryStages.reduce((sum, s) => sum + s.items.length, 0)
)

function getProgressColor(progress: number): string {
  if (progress >= 90) return '#67c23a'
  if (progress >= 60) return '#409eff'
  if (progress >= 30) return '#e6a23c'
  return '#f56c6c'
}

// Drag state
let draggedItem: ProjectItem | null = null
let draggedFromStage: string | null = null

function onDragStart(event: DragEvent, item: ProjectItem, stageKey: string) {
  draggedItem = item
  draggedFromStage = stageKey
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', item.id.toString())
  }
}

function onDragOver(event: DragEvent) {
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
}

function onDrop(event: DragEvent, targetStageKey: string) {
  if (!draggedItem || !draggedFromStage || draggedFromStage === targetStageKey) {
    draggedItem = null
    draggedFromStage = null
    return
  }

  // Find and remove from source
  const allStageGroups = [preSalesStages, contractStages, deliveryStages]
  let sourceStage: KanbanStage | undefined

  for (const group of allStageGroups) {
    sourceStage = group.find((s) => s.key === draggedFromStage!)
    if (sourceStage) break
  }

  if (!sourceStage) {
    draggedItem = null
    draggedFromStage = null
    return
  }

  const itemIndex = sourceStage.items.findIndex((i) => i.id === draggedItem!.id)
  if (itemIndex !== -1) {
    const [removed] = sourceStage.items.splice(itemIndex, 1)

    // Add to target
    let targetStage: KanbanStage | undefined
    for (const group of allStageGroups) {
      targetStage = group.find((s) => s.key === targetStageKey)
      if (targetStage) break
    }

    if (targetStage) {
      targetStage.items.push(removed)
    } else {
      // Put back if target not found
      sourceStage.items.splice(itemIndex, 0, removed)
    }
  }

  draggedItem = null
  draggedFromStage = null
}
</script>

<style scoped lang="scss">
.projects-page {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;

    h2 {
      margin: 0;
      font-size: 22px;
      font-weight: 600;
      color: #303133;
    }
  }

  .stage-section {
    margin-bottom: 28px;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
    padding-left: 4px;

    .section-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      flex-shrink: 0;
    }

    .section-title {
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }

    .section-count {
      font-size: 12px;
      color: #909399;
      margin-left: 8px;
    }
  }

  .kanban-board {
    overflow-x: auto;
    padding-bottom: 4px;
  }

  .kanban-row {
    flex-wrap: nowrap;
    min-width: max-content;
  }

  .kanban-column {
    width: 100%;
    min-height: 340px;
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
  }

  .column-body {
    padding: 12px;
    min-height: 160px;
  }

  .project-card {
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
      word-break: break-all;
    }

    &__info {
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-bottom: 10px;

      .info-row {
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
    }

    &__progress {
      .progress-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
        font-size: 11px;
        color: #909399;

        .progress-value {
          font-weight: 500;
          color: #303133;
        }
      }
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
    height: 100px;
    color: #c0c4cc;
    font-size: 13px;
    border: 1px dashed #e4e7ed;
    border-radius: 4px;
  }
}
</style>
