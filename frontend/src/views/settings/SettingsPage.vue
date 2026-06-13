<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { UploadFile, FormInstance, FormRules } from 'element-plus'

// ---- 标签页 ----
type SettingsTab = 'profile' | 'team' | 'notification' | 'system'
const activeTab = ref<SettingsTab>('profile')

// ==================== 个人信息 ====================
const profileFormRef = ref<FormInstance>()
const profileForm = reactive({
  name: '李经理',
  email: 'lijingli@example.com',
  phone: '13800138000',
  avatar: '',
  department: '销售一部',
  position: '高级客户经理',
})

const profileRules: FormRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在2-20个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' },
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' },
  ],
}

const avatarFileList = ref<UploadFile[]>([])

function handleSaveProfile(formEl: FormInstance | undefined) {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      ElMessage.success('个人信息保存成功')
    }
  })
}

function handleAvatarChange(file: UploadFile) {
  // 模拟头像更新
  ElMessage.success('头像已更新')
}

// ==================== 团队管理 ====================
interface TeamMember {
  id: number
  name: string
  email: string
  role: 'admin' | 'manager' | 'member'
  department: string
  joinDate: string
}

const teamMembers = ref<TeamMember[]>([
  { id: 1, name: '李经理', email: 'lijingli@example.com', role: 'admin', department: '销售一部', joinDate: '2024-01-10' },
  { id: 2, name: '王总监', email: 'wangzong@example.com', role: 'admin', department: '技术部', joinDate: '2024-02-15' },
  { id: 3, name: '张销售', email: 'zhangxs@example.com', role: 'manager', department: '销售一部', joinDate: '2024-03-20' },
  { id: 4, name: '赵助理', email: 'zhaozl@example.com', role: 'member', department: '销售二部', joinDate: '2025-01-05' },
  { id: 5, name: '刘工', email: 'liug@example.com', role: 'member', department: '技术部', joinDate: '2025-04-12' },
  { id: 6, name: '陈运维', email: 'chenyw@example.com', role: 'member', department: '技术部', joinDate: '2025-06-01' },
  { id: 7, name: '周法务', email: 'zhoufw@example.com', role: 'member', department: '法务部', joinDate: '2025-08-15' },
])

const roleLabels: Record<string, string> = {
  admin: '管理员',
  manager: '经理',
  member: '成员',
}

const roleTagTypes: Record<string, '' | 'danger' | 'warning' | 'info'> = {
  admin: 'danger',
  manager: 'warning',
  member: 'info',
}

const addMemberVisible = ref(false)
const addMemberForm = reactive({
  name: '',
  email: '',
  role: 'member' as TeamMember['role'],
  department: '',
})

function handleAddMember() {
  if (!addMemberForm.name || !addMemberForm.email) {
    ElMessage.warning('请填写姓名和邮箱')
    return
  }
  const newMember: TeamMember = {
    id: Date.now(),
    name: addMemberForm.name,
    email: addMemberForm.email,
    role: addMemberForm.role,
    department: addMemberForm.department || '未分配',
    joinDate: new Date().toISOString().slice(0, 10),
  }
  teamMembers.value.push(newMember)
  addMemberVisible.value = false
  addMemberForm.name = ''
  addMemberForm.email = ''
  addMemberForm.role = 'member'
  addMemberForm.department = ''
  ElMessage.success('成员添加成功')
}

function handleRemoveMember(member: TeamMember) {
  ElMessageBox.confirm(
    `确认将「${member.name}」移出团队？此操作不可撤销。`,
    '移除成员',
    { confirmButtonText: '确认移除', cancelButtonText: '取消', type: 'warning' },
  )
    .then(() => {
      teamMembers.value = teamMembers.value.filter((m) => m.id !== member.id)
      ElMessage.success('成员已移除')
    })
    .catch(() => {})
}

// ==================== 通知设置 ====================
const notifications = reactive({
  // 邮件通知
  emailDailyReport: true,
  emailWeeklyReport: true,
  emailMonthlyReport: true,
  emailTaskReminder: true,
  emailSystemNotice: false,
  // 飞书通知
  feishuDailyReport: false,
  feishuTaskReminder: true,
  feishuApprovalNotify: true,
  feishuMentionNotify: true,
  // 系统通知
  systemUpdateNotify: true,
  systemMaintenanceNotify: false,
  systemSecurityAlert: true,
})

function handleNotificationChange(_value: boolean) {
  // 通知状态变更持久化
}

// ==================== 系统配置 ====================
const systemFormRef = ref<FormInstance>()
const systemConfig = reactive({
  dataRetentionDays: 365,
  defaultLanguage: 'zh-CN',
  timezone: 'Asia/Shanghai',
  sessionTimeout: 480,
  logLevel: 'info',
  autoBackup: true,
  backupInterval: 24,
})

const languageOptions = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' },
  { label: '日本語', value: 'ja-JP' },
]

const timezoneOptions = [
  { label: '亚洲/上海 (UTC+8)', value: 'Asia/Shanghai' },
  { label: '亚洲/东京 (UTC+9)', value: 'Asia/Tokyo' },
  { label: '美洲/纽约 (UTC-5)', value: 'America/New_York' },
  { label: '欧洲/伦敦 (UTC+0)', value: 'Europe/London' },
]

const logLevelOptions = [
  { label: 'DEBUG', value: 'debug' },
  { label: 'INFO', value: 'info' },
  { label: 'WARN', value: 'warn' },
  { label: 'ERROR', value: 'error' },
]

function handleSaveSystem(formEl: FormInstance | undefined) {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      ElMessage.success('系统配置保存成功')
    }
  })
}

function handleResetSystem(formEl: FormInstance | undefined) {
  ElMessageBox.confirm('确认恢复默认配置？当前修改将丢失。', '恢复默认', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    systemConfig.dataRetentionDays = 365
    systemConfig.defaultLanguage = 'zh-CN'
    systemConfig.timezone = 'Asia/Shanghai'
    systemConfig.sessionTimeout = 480
    systemConfig.logLevel = 'info'
    systemConfig.autoBackup = true
    systemConfig.backupInterval = 24
    ElMessage.success('已恢复默认配置')
  }).catch(() => {})
}
</script>

<template>
  <div class="settings-page">
    <h2 class="page-title">系统设置</h2>

    <el-tabs v-model="activeTab" class="settings-tabs">
      <!-- 个人信息 -->
      <el-tab-pane label="个人信息" name="profile">
        <el-card shadow="hover" class="section-card">
          <el-row :gutter="40">
            <el-col :span="12">
              <el-form
                ref="profileFormRef"
                :model="profileForm"
                :rules="profileRules"
                label-width="80px"
                label-position="top"
              >
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="profileForm.name" />
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="profileForm.email" />
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                  <el-input v-model="profileForm.phone" />
                </el-form-item>
                <el-form-item label="部门">
                  <el-input v-model="profileForm.department" disabled />
                </el-form-item>
                <el-form-item label="职位">
                  <el-input v-model="profileForm.position" disabled />
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="12">
              <div class="avatar-section">
                <p class="field-label">头像</p>
                <el-avatar :size="100" src="" class="avatar-preview">
                  <el-icon :size="40"><UserFilled /></el-icon>
                </el-avatar>
                <el-upload
                  v-model:file-list="avatarFileList"
                  :limit="1"
                  :auto-upload="false"
                  :show-file-list="false"
                  :on-change="handleAvatarChange"
                  accept="image/png,image/jpeg,image/gif"
                >
                  <el-button type="primary" size="small" style="margin-top: 12px">
                    更换头像
                  </el-button>
                </el-upload>
                <p class="upload-tip">支持 JPG/PNG/GIF，不超过 2MB</p>
              </div>
            </el-col>
          </el-row>
          <div class="form-footer">
            <el-button type="primary" @click="handleSaveProfile(profileFormRef)">
              保存修改
            </el-button>
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 团队管理 -->
      <el-tab-pane label="团队管理" name="team">
        <el-card shadow="hover" class="section-card">
          <div class="table-toolbar">
            <span class="member-count">成员总数：{{ teamMembers.length }}</span>
            <el-button type="primary" size="small" @click="addMemberVisible = true">
              <el-icon><Plus /></el-icon>添加成员
            </el-button>
          </div>
          <el-table :data="teamMembers" stripe style="width: 100%">
            <el-table-column prop="name" label="姓名" width="120" />
            <el-table-column prop="email" label="邮箱" min-width="200" />
            <el-table-column prop="role" label="角色" width="100" align="center">
              <template #default="{ row }">
                <el-tag size="small" :type="roleTagTypes[row.role]" effect="plain">
                  {{ roleLabels[row.role] }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="department" label="部门" width="130" />
            <el-table-column prop="joinDate" label="加入时间" width="120" align="center" />
            <el-table-column label="操作" width="100" align="center">
              <template #default="{ row }">
                <el-button
                  type="danger"
                  size="small"
                  link
                  :disabled="row.role === 'admin'"
                  @click="handleRemoveMember(row)"
                >
                  移除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <!-- 添加成员弹窗 -->
        <el-dialog v-model="addMemberVisible" title="添加团队成员" width="480px" destroy-on-close>
          <el-form label-width="80px">
            <el-form-item label="姓名" required>
              <el-input v-model="addMemberForm.name" placeholder="请输入姓名" />
            </el-form-item>
            <el-form-item label="邮箱" required>
              <el-input v-model="addMemberForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="角色">
              <el-select v-model="addMemberForm.role" style="width: 100%">
                <el-option label="管理员" value="admin" />
                <el-option label="经理" value="manager" />
                <el-option label="成员" value="member" />
              </el-select>
            </el-form-item>
            <el-form-item label="部门">
              <el-input v-model="addMemberForm.department" placeholder="请输入部门（选填）" />
            </el-form-item>
          </el-form>
          <template #footer>
            <el-button @click="addMemberVisible = false">取消</el-button>
            <el-button type="primary" @click="handleAddMember">确认添加</el-button>
          </template>
        </el-dialog>
      </el-tab-pane>

      <!-- 通知设置 -->
      <el-tab-pane label="通知设置" name="notification">
        <el-card shadow="hover" class="section-card">
          <div class="notification-group">
            <h3 class="group-title">
              <el-icon color="#409EFF"><Message /></el-icon>邮件通知
            </h3>
            <div class="switch-list">
              <div class="switch-item">
                <div>
                  <p class="switch-label">日报推送</p>
                  <p class="switch-desc">每日18:00自动发送工作日报汇总</p>
                </div>
                <el-switch v-model="notifications.emailDailyReport" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">周报推送</p>
                  <p class="switch-desc">每周五18:00发送本周工作汇总</p>
                </div>
                <el-switch v-model="notifications.emailWeeklyReport" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">月报推送</p>
                  <p class="switch-desc">每月最后一天18:00发送月度报告</p>
                </div>
                <el-switch v-model="notifications.emailMonthlyReport" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">任务提醒</p>
                  <p class="switch-desc">待办任务到期前2小时发送提醒邮件</p>
                </div>
                <el-switch v-model="notifications.emailTaskReminder" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">系统公告</p>
                  <p class="switch-desc">系统升级、维护等重要公告邮件通知</p>
                </div>
                <el-switch v-model="notifications.emailSystemNotice" @change="handleNotificationChange" />
              </div>
            </div>
          </div>

          <el-divider />

          <div class="notification-group">
            <h3 class="group-title">
              <el-icon color="#67C23A"><Promotion /></el-icon>飞书通知
            </h3>
            <div class="switch-list">
              <div class="switch-item">
                <div>
                  <p class="switch-label">日报推送</p>
                  <p class="switch-desc">通过飞书机器人发送工作日报</p>
                </div>
                <el-switch v-model="notifications.feishuDailyReport" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">任务提醒</p>
                  <p class="switch-desc">待办任务通过飞书消息提醒</p>
                </div>
                <el-switch v-model="notifications.feishuTaskReminder" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">审批通知</p>
                  <p class="switch-desc">合同审批、方案审批等流程通知</p>
                </div>
                <el-switch v-model="notifications.feishuApprovalNotify" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">@提醒</p>
                  <p class="switch-desc">同事在飞书中@你时同步通知</p>
                </div>
                <el-switch v-model="notifications.feishuMentionNotify" @change="handleNotificationChange" />
              </div>
            </div>
          </div>

          <el-divider />

          <div class="notification-group">
            <h3 class="group-title">
              <el-icon color="#E6A23C"><BellFilled /></el-icon>系统通知
            </h3>
            <div class="switch-list">
              <div class="switch-item">
                <div>
                  <p class="switch-label">系统更新通知</p>
                  <p class="switch-desc">版本更新、新功能上线时推送通知</p>
                </div>
                <el-switch v-model="notifications.systemUpdateNotify" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">维护通知</p>
                  <p class="switch-desc">系统维护窗口和停机通知</p>
                </div>
                <el-switch v-model="notifications.systemMaintenanceNotify" @change="handleNotificationChange" />
              </div>
              <div class="switch-item">
                <div>
                  <p class="switch-label">安全告警</p>
                  <p class="switch-desc">异常登录、权限变更等安全告警</p>
                </div>
                <el-switch v-model="notifications.systemSecurityAlert" @change="handleNotificationChange" />
              </div>
            </div>
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 系统配置 -->
      <el-tab-pane label="系统配置" name="system">
        <el-card shadow="hover" class="section-card">
          <el-form
            ref="systemFormRef"
            :model="systemConfig"
            label-width="160px"
            label-position="left"
          >
            <el-form-item label="数据保留天数">
              <el-input-number
                v-model="systemConfig.dataRetentionDays"
                :min="30"
                :max="3650"
                :step="30"
                controls-position="right"
              />
              <span class="form-hint">超过期限的数据将被自动归档或删除</span>
            </el-form-item>

            <el-form-item label="默认语言">
              <el-select v-model="systemConfig.defaultLanguage" style="width: 240px">
                <el-option
                  v-for="opt in languageOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="时区">
              <el-select v-model="systemConfig.timezone" style="width: 320px">
                <el-option
                  v-for="opt in timezoneOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="会话超时时间（分钟）">
              <el-input-number
                v-model="systemConfig.sessionTimeout"
                :min="5"
                :max="1440"
                :step="30"
                controls-position="right"
              />
              <span class="form-hint">超时后用户需重新登录</span>
            </el-form-item>

            <el-form-item label="日志级别">
              <el-select v-model="systemConfig.logLevel" style="width: 200px">
                <el-option
                  v-for="opt in logLevelOptions"
                  :key="opt.value"
                  :label="opt.label"
                  :value="opt.value"
                />
              </el-select>
            </el-form-item>

            <el-divider />

            <el-form-item label="自动备份">
              <el-switch v-model="systemConfig.autoBackup" />
              <span class="form-hint">启用后系统将按设定周期自动备份数据</span>
            </el-form-item>

            <el-form-item label="备份间隔（小时）" v-if="systemConfig.autoBackup">
              <el-input-number
                v-model="systemConfig.backupInterval"
                :min="1"
                :max="168"
                :step="1"
                controls-position="right"
              />
            </el-form-item>
          </el-form>

          <div class="form-footer">
            <el-button @click="handleResetSystem(systemFormRef)">恢复默认</el-button>
            <el-button type="primary" @click="handleSaveSystem(systemFormRef)">保存配置</el-button>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped lang="scss">
.settings-page {
  max-width: 900px;
  margin: 0 auto;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #303133;
}

.settings-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
}

.section-card {
  .form-footer {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #f0f0f0;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
}

// ---- 个人信息 ----
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 8px;

  .field-label {
    font-size: 14px;
    color: #606266;
    margin-bottom: 12px;
    text-align: center;
    width: 100%;
  }

  .avatar-preview {
    border: 2px solid #e4e7ed;
  }

  .upload-tip {
    margin-top: 8px;
    font-size: 12px;
    color: #c0c4cc;
  }
}

// ---- 团队管理 ----
.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;

  .member-count {
    font-size: 14px;
    color: #606266;
    font-weight: 500;
  }
}

// ---- 通知设置 ----
.notification-group {
  .group-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 16px;
  }
}

.switch-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.switch-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-radius: 8px;
  transition: background-color 0.2s;

  &:hover {
    background-color: #fafafa;
  }

  .switch-label {
    font-size: 14px;
    color: #303133;
    font-weight: 500;
    margin-bottom: 2px;
  }

  .switch-desc {
    font-size: 12px;
    color: #909399;
    margin: 0;
  }
}

// ---- 系统配置 ----
.form-hint {
  margin-left: 12px;
  font-size: 13px;
  color: #909399;
}
</style>
