import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { setupAuthGuard } from './authGuard'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/LoginPage.vue'),
    meta: { title: '登录', hidden: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/DashboardPage.vue'),
    meta: { title: '运营数据驾驶舱', icon: 'Odometer' },
  },
  {
    path: '/customers',
    name: 'Customers',
    component: () => import('@/views/customers/CustomerListPage.vue'),
    meta: { title: '客户列表', icon: 'User' },
  },
  {
    path: '/customers/:id',
    name: 'CustomerDetail',
    component: () => import('@/views/customers/CustomerDetailPage.vue'),
    meta: { title: '客户详情', hidden: true },
  },
  {
    path: '/bidding',
    name: 'Bidding',
    component: () => import('@/views/bidding/BiddingPage.vue'),
    meta: { title: '招投标管理', icon: 'Document' },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('@/views/projects/ProjectsPage.vue'),
    meta: { title: '项目管理', icon: 'List' },
  },
  {
    path: '/relationships',
    name: 'Relationships',
    component: () => import('@/views/relationships/RelationshipsPage.vue'),
    meta: { title: '关系维护', icon: 'Connection' },
  },
  {
    path: '/contracts',
    name: 'Contracts',
    component: () => import('@/views/contracts/ContractPage.vue'),
    meta: { title: '合同管理', icon: 'Tickets' },
  },
  {
    path: '/acceptance',
    name: 'Acceptance',
    component: () => import('@/views/acceptance/AcceptancePage.vue'),
    meta: { title: '验收管理', icon: 'Checked' },
  },
  {
    path: '/ltc',
    name: 'LTC',
    component: () => import('@/views/ltc/LtcPage.vue'),
    meta: { title: 'LTC全链路', icon: 'TrendCharts' },
  },
  {
    path: '/ai-reports',
    name: 'AIReports',
    component: () => import('@/views/ai-reports/AIReportsPage.vue'),
    meta: { title: '工作总结', icon: 'EditPen' },
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/knowledge/KnowledgePage.vue'),
    meta: { title: '知识库管理', icon: 'Collection' },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/settings/SettingsPage.vue'),
    meta: { title: '系统设置', icon: 'Setting' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundPage.vue'),
    meta: { title: '404', hidden: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

setupAuthGuard(router)

export default router
