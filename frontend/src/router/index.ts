import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/dashboard',
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
    path: '/acceptance',
    name: 'Acceptance',
    component: () => import('@/views/acceptance/AcceptancePage.vue'),
    meta: { title: '验收管理', icon: 'Checked' },
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

export default router
