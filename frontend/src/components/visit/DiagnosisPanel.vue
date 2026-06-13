<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ customerId?: number }>()

interface Signal { text: string; level: 'danger' | 'warning' | 'info'; source: string; date: string }
interface Script { text: string; targetRole: string }

const panels = ref([
  {
    key: 'overview', title: '客户全景', icon: 'DataAnalysis',
    content: { name: '中科曙光', industry: 'IT/互联网', level: 'A级', totalVisits: 24, lastVisit: '2026-06-10', totalOrders: '1568万', relationScore: 68 },
  },
  {
    key: 'diagnosis', title: '问题诊断', icon: 'WarningFilled', color: '#F56C6C',
    signals: [
      { text: '近30天互动频次下降40%，关系温度降温', level: 'danger' as const, source: 'AI行为分析', date: '2026-06-12' },
      { text: '竞争对手华为云已拜访决策链关键人张总', level: 'danger' as const, source: '竞品监控', date: '2026-06-10' },
      { text: '上一期合同还有45天到期，尚未收到续约意向', level: 'warning' as const, source: '合同系统', date: '2026-06-08' },
      { text: '决策链中缺少技术评估角色（未覆盖刘工）', level: 'warning' as const, source: '决策链分析', date: '2026-06-05' },
    ],
  },
  {
    key: 'advice', title: '行动建议', icon: 'CircleCheck', color: '#67C23A',
    signals: [
      { text: '安排高层互访：我方CTO拜访对方张总', level: 'info' as const, source: 'AI策略引擎', date: '2026-06-13' },
      { text: '针对华为此前拜访内容，准备技术对比材料', level: 'info' as const, source: '竞品分析', date: '2026-06-13' },
      { text: '提前30天启动续约谈判流程', level: 'info' as const, source: '合同预警', date: '2026-06-12' },
    ],
  },
  {
    key: 'risk', title: '风险预警', icon: 'Bell', color: '#E6A23C',
    signals: [
      { text: '⚠️ 高阶: 客户流失概率62%（中高危）', level: 'danger' as const, source: 'AI预测模型', date: '2026-06-13' },
      { text: '⚠️ 中阶: 付款逾期风险，上一笔回款超时15天', level: 'warning' as const, source: '财务系统', date: '2026-06-11' },
    ],
  },
  {
    key: 'script', title: '建议话术', icon: 'ChatLineSquare',
    scripts: [
      { text: '张总，上次您提到对AI运维模块很感兴趣，我们这次带来了一个具体的POC方案，可以两周内让您看到效果。', targetRole: '经济决策者' },
      { text: '王工，关于您上次提的三个技术建议，我们已经在v3.2.1版本中全部纳入了，这次可以详细演示。', targetRole: '技术决策者' },
      { text: '赵经理，新的平台会大幅减少您团队的手工操作，初步测算可以节省30%的日常运维工时。', targetRole: '使用者' },
    ],
  },
])

const activePanel = ref('diagnosis')
</script>

<template>
  <div class="diagnosis-panel">
    <el-tabs v-model="activePanel" type="border-card">
      <el-tab-pane v-for="p in panels" :key="p.key" :label="p.title">
        <!-- 客户全景 -->
        <template v-if="p.key === 'overview' && p.content">
          <el-descriptions :column="2" border size="small">
            <el-descriptions-item v-for="(v, k) in p.content" :key="k" :label="k">{{ v }}</el-descriptions-item>
          </el-descriptions>
        </template>

        <!-- 信号列表 -->
        <template v-if="p.signals">
          <div v-for="(s, i) in p.signals" :key="i" class="signal-item" :style="{ borderLeftColor: s.level === 'danger' ? '#F56C6C' : s.level === 'warning' ? '#E6A23C' : '#409EFF' }">
            <el-tag :type="s.level" size="small">{{ s.level === 'danger' ? '严重' : s.level === 'warning' ? '警告' : '建议' }}</el-tag>
            <span class="signal-text">{{ s.text }}</span>
            <div class="signal-meta">{{ s.source }} · {{ s.date }}</div>
          </div>
        </template>

        <!-- 话术 -->
        <template v-if="p.scripts">
          <div v-for="(s, i) in p.scripts" :key="i" class="script-item">
            <el-tag size="small" type="primary">{{ s.targetRole }}</el-tag>
            <p class="script-text">"{{ s.text }}"</p>
          </div>
        </template>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped lang="scss">
.signal-item { padding: 10px 12px; margin-bottom: 8px; border-left: 3px solid; background: #fafafa; border-radius: 4px; }
.signal-text { display: block; margin: 4px 0; font-size: 14px; }
.signal-meta { font-size: 12px; color: #909399; }
.script-item { padding: 12px; margin-bottom: 8px; background: #f0f9ff; border-radius: 8px; }
.script-text { margin: 8px 0 0; font-size: 14px; font-style: italic; color: #333; line-height: 1.6; }
</style>
