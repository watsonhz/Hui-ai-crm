import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

/** 路由守卫：未登录自动跳转 /login */
export function setupAuthGuard(router: Router) {
  router.beforeEach((to, _from, next) => {
    const auth = useAuthStore()

    // 白名单：无需登录即可访问
    const whitelist = ['/login']
    if (whitelist.includes(to.path)) {
      if (auth.isLoggedIn && to.path === '/login') return next('/dashboard')
      return next()
    }

    // 其他页面需要登录
    if (!auth.isLoggedIn) {
      return next({ path: '/login', query: { redirect: to.fullPath } })
    }

    next()
  })
}
