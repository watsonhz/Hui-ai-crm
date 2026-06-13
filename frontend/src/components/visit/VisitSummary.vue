<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useVisitStore } from '@/stores/visit'

const emit = defineEmits<{ prev: [] }>()
const store = useVisitStore()

const nextVisitDate = ref('')

const formattedMinutes = ref(`# 拜访纪要：${store.visitInfo.customerName}

**时间：** ${store.visitInfo.visitTime}
**地点：** ${store.visitInfo.location}
**我方参会：** ${store.visitInfo.ourAttendees}
**客户参会：** ${store.visitInfo.customerAttendees}

## 一、拜访摘要
本次${store.visitInfo.stage}拜访按计划进行。客户对我方整体方案表示认可，沟通氛围良好。

## 二、关键决策
1. 客户确认项目优先级，同意加速推进
2. 技术方案细节经沟通达成一致
3. 商务条款需进一步协商

## 三、客户关注点
- AI运维能力模块的技术细节
- 项目实施周期和人员安排
- 售后服务和SLA条款

## 四、客户态度
${store.customerAttitude ? `${store.customerAttitude} / 关系${store.relationTrend || '稳定'}` : '尚未记录'}
`)

function handleScheduleVisit() {
  if (!nextVisitDate.value) {
    ElMessage.warning('请先选择下次拜访时间')
    return
  }
  ElMessage.success(`下次拜访已预约: ${nextVisitDate.value}`)
}
</script>

<template>
  <div class="summary-screen">
    <el-row :gutter="20">
      <!-- 左栏：AI 纪要（可编辑） -->
      <el-col :span="14">
        <el-card shadow="hover" class="minutes-card">
          <template #header>
            <span class="card-title">AI 生成纪要</span>
            <div class="card-actions">
              <el-button size="small" text type="primary">🔄 重新生成</el-button>
              <el-button size="small" text type="success">📋 复制</el-button>
            </div>
          </template>
          <el-input
            v-model="formattedMinutes" type="textarea" :rows="20"
            class="minutes-editor"
          />
        </el-card>
      </el-col>

      <!-- 右栏：行动项 -->
      <el-col :span="10">
        <el-card shadow="hover" class="actions-card">
          <template #header>
            <span class="card-title">AI 行动项</span>
            <el-tooltip content="AI根据拜访内容自动生成">
              <el-tag size="small" type="info">🤖 自动生成</el-tag>
            </el-tooltip>
          </template>

          <div v-for="item in store.actionItems" :key="item.id" class="action-card">
            <div class="action-header">
              <el-tag
                :type="item.priority === 'P0' ? 'danger' : item.priority === 'P1' ? 'warning' : 'info'"
                size="small"
              >
                {{ item.priority }}
              </el-tag>
              <el-switch v-model="item.done" size="small" />
            </div>
            <p class="action-text">{{ item.content }}</p>
            <div class="action-meta">
              <el-icon :size="14"><User /></el-icon>
              <span>{{ item.assignee }}</span>
              <el-icon :size="14" style="margin-left:12px"><Calendar /></el-icon>
              <span>{{ item.due }}</span>
            </div>
          </div>

          <!-- 预约下次拜访 -->
          <el-divider />
          <div class="next-visit-section">
            <p class="next-visit-title">📅 预约下次拜访</p>
            <el-date-picker
              v-model="nextVisitDate" type="datetime" placeholder="选择时间"
              style="width: 100%" value-format="YYYY-MM-DD HH:mm:ss"
            />
            <el-button type="primary" style="width:100%;margin-top:8px" @click="handleScheduleVisit">
              确认预约
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 底部 -->
    <div class="bottom-bar">
      <el-button size="large" @click="emit('prev')">上一步</el-button>
      <el-button type="success" size="large" @click="ElMessage.success('拜访完成！纪要已保存')">
        完成拜访 <el-icon><Check /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.summary-screen { max-width: 1200px; margin: 0 auto; }
.minutes-card, .actions-card { height: 100%; }
.card-title { font-size: 15px; font-weight: 600; }
.card-actions { float: right; display: flex; gap: 8px; }
.minutes-editor textarea { font-family: 'Microsoft YaHei', sans-serif; font-size: 14px; line-height: 1.8; }
.action-card {
  padding: 12px; margin-bottom: 12px;
  border: 1px solid #e8e8e8; border-radius: 8px; background: #fafafa;
}
.action-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.action-text { font-size: 14px; color: #333; margin: 0 0 6px; }
.action-meta { display: flex; align-items: center; gap: 4px; font-size: 12px; color: #909399; }
.next-visit-section { .next-visit-title { font-size: 14px; font-weight: 600; margin-bottom: 8px; } }
.bottom-bar { display: flex; justify-content: center; gap: 16px; padding: 20px 0; }
</style>
