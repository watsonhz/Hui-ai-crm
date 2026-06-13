import { ElMessage, ElNotification } from 'element-plus'

/** 统一 Toast 通知封装 */
export const toast = {
  success(msg: string) { ElMessage.success(msg) },
  error(msg: string) { ElMessage.error(msg) },
  warning(msg: string) { ElMessage.warning(msg) },
  info(msg: string) { ElMessage.info(msg) },
  notify(title: string, message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info') {
    ElNotification({ title, message, type, duration: 4000 })
  },
}
