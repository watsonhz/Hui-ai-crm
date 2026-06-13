<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goHome() {
  router.push('/dashboard')
}
</script>

<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <el-result
        icon="warning"
        title="404"
        sub-title="页面不存在"
      >
        <template #extra>
          <p class="description-text">
            您访问的页面可能已被移动、删除或地址输入有误
          </p>
          <el-button type="primary" size="large" @click="goHome">
            <el-icon><HomeFilled /></el-icon>
            返回首页
          </el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style scoped lang="scss">
.not-found-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 120px);
  padding: 40px 20px;
}

.not-found-content {
  text-align: center;

  :deep(.el-result) {
    padding: 0;

    .el-result__icon {
      svg {
        width: 80px;
        height: 80px;
        color: #e6a23c;
      }
    }

    .el-result__title {
      font-size: 96px;
      font-weight: 800;
      color: #303133;
      line-height: 1.1;
      margin-top: 16px;
      letter-spacing: -2px;
    }

    .el-result__subtitle {
      font-size: 20px;
      color: #606266;
      margin-top: 12px;
      font-weight: 500;
    }
  }

  .description-text {
    font-size: 14px;
    color: #909399;
    margin-bottom: 24px;
    margin-top: -8px;
  }
}
</style>
