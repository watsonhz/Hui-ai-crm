<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const loginMode = ref<'password' | 'wechat' | 'sms'>('password')
const loading = ref(false)
const rememberMe = ref(false)
const countdown = ref(0)

// 密码登录
const passwordForm = reactive({ username: '', password: '' })

// 短信登录
const smsForm = reactive({ phone: '', code: '' })

function startCountdown() {
  countdown.value = 60
  const timer = setInterval(() => { countdown.value--; if (countdown.value <= 0) clearInterval(timer) }, 1000)
}

async function handlePasswordLogin() {
  if (!passwordForm.username || !passwordForm.password) { ElMessage.warning('请输入用户名和密码'); return }
  loading.value = true
  await new Promise(r => setTimeout(r, 800))
  // Mock JWT login
  auth.setAuth('mock-jwt-token-xyz', { name: '管理员', role: 'admin', avatar: '' })
  ElMessage.success('登录成功')
  loading.value = false
  const redirect = (route.query.redirect as string) || '/dashboard'
  router.push(redirect)
}

async function handleSmsLogin() {
  if (!smsForm.phone || !smsForm.code) { ElMessage.warning('请输入手机号和验证码'); return }
  loading.value = true
  await new Promise(r => setTimeout(r, 500))
  auth.setAuth('mock-jwt-sms-token', { name: '管理员', role: 'admin' })
  ElMessage.success('登录成功')
  loading.value = false
  router.push((route.query.redirect as string) || '/dashboard')
}

function sendSms() {
  if (!/^1[3-9]\d{9}$/.test(smsForm.phone)) { ElMessage.warning('请输入正确的手机号'); return }
  startCountdown()
  ElMessage.success('验证码已发送')
}

function handleWechatLogin() {
  ElMessage.info('请使用微信扫描二维码（演示模式：3秒后自动登录）')
  setTimeout(() => {
    auth.setAuth('mock-jwt-wechat-token', { name: '微信用户', role: 'user' })
    ElMessage.success('微信登录成功')
    router.push((route.query.redirect as string) || '/dashboard')
  }, 3000)
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Logo -->
      <div class="login-header">
        <el-icon :size="40" color="#409EFF"><Cpu /></el-icon>
        <h1>AI CRM</h1>
        <p>智能客户关系管理系统</p>
      </div>

      <!-- Tab 切换 -->
      <div class="login-tabs">
        <span :class="{ active: loginMode === 'password' }" @click="loginMode = 'password'">密码登录</span>
        <span :class="{ active: loginMode === 'wechat' }" @click="loginMode = 'wechat'">微信登录</span>
        <span :class="{ active: loginMode === 'sms' }" @click="loginMode = 'sms'">短信登录</span>
      </div>

      <!-- 密码登录 -->
      <div v-if="loginMode === 'password'" class="login-form">
        <el-input v-model="passwordForm.username" placeholder="用户名 / 邮箱" size="large" clearable>
          <template #prefix><el-icon><User /></el-icon></template>
        </el-input>
        <el-input v-model="passwordForm.password" type="password" placeholder="密码" size="large" show-password>
          <template #prefix><el-icon><Lock /></el-icon></template>
        </el-input>
        <div class="form-extra">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <a href="#" class="forgot-link">忘记密码？</a>
        </div>
        <el-button type="primary" size="large" :loading="loading" class="login-btn" @click="handlePasswordLogin">
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </div>

      <!-- 微信扫码登录 -->
      <div v-if="loginMode === 'wechat'" class="wechat-section">
        <div class="qr-placeholder" @click="handleWechatLogin">
          <el-icon :size="80" color="#07C160"><ChatDotSquare /></el-icon>
          <p>微信扫码登录</p>
          <el-tag size="small" type="info">点击模拟扫码</el-tag>
        </div>
      </div>

      <!-- 短信登录 -->
      <div v-if="loginMode === 'sms'" class="login-form">
        <el-input v-model="smsForm.phone" placeholder="手机号" size="large">
          <template #prefix><el-icon><Iphone /></el-icon></template>
        </el-input>
        <div class="sms-row">
          <el-input v-model="smsForm.code" placeholder="验证码" size="large" style="flex:1">
            <template #prefix><el-icon><Message /></el-icon></template>
          </el-input>
          <el-button size="large" :disabled="countdown > 0" @click="sendSms" style="margin-left:12px;min-width:120px">
            {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
          </el-button>
        </div>
        <el-button type="primary" size="large" :loading="loading" class="login-btn" @click="handleSmsLogin">
          {{ loading ? '登录中...' : '登 录' }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.login-container {
  min-height: 100vh; display: flex; align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 50% 0%, #1e3a5f 0%, #0b1120 60%);
}
.login-card {
  width: 420px; background: #fff; border-radius: 16px; padding: 40px;
  box-shadow: 0 20px 60px rgba(0,0,0,.15);
}
.login-header { text-align: center; margin-bottom: 30px; h1 { margin: 8px 0 4px; font-size: 24px; } p { color: #909399; margin: 0; } }
.login-tabs { display: flex; justify-content: center; gap: 24px; margin-bottom: 24px;
  span { cursor: pointer; padding: 8px 0; font-size: 14px; color: #909399; border-bottom: 2px solid transparent; transition: .2s;
    &.active { color: #409EFF; border-bottom-color: #409EFF; font-weight: 600; }
  }
}
.login-form { display: flex; flex-direction: column; gap: 16px; }
.form-extra { display: flex; justify-content: space-between; align-items: center; font-size: 13px;
  .forgot-link { color: #409EFF; text-decoration: none; }
}
.login-btn { width: 100%; height: 44px; font-size: 16px; }
.sms-row { display: flex; }
.wechat-section { text-align: center; padding: 30px 0; }
.qr-placeholder {
  display: inline-flex; flex-direction: column; align-items: center; gap: 12px;
  width: 200px; height: 200px; border: 2px dashed #ddd; border-radius: 12px;
  justify-content: center; cursor: pointer; color: #07C160;
  &:hover { border-color: #07C160; background: #f0fdf4; }
  p { margin: 0; font-weight: 600; }
}
</style>
