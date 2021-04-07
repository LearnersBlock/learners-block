import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Home.vue'), name: 'home' },
      { path: '/login', component: () => import('pages/Login.vue'), name: 'login' },
      { path: '/password_reset', component: () => import('pages/ResetPassword.vue'), name: 'password_reset' },
      { path: '/settings', component: () => import('pages/Settings.vue'), name: 'settings' },
      { path: '/captive-portal', component: () => import('pages/CaptivePortal.vue'), name: 'captive-portal' },
      { path: '/makerspace', component: () => import('pages/Makerspace.vue'), name: 'makerspace' },
      { path: '/library', component: () => import('pages/Library.vue'), name: 'library' },
      { path: '/401', component: () => import('pages/401.vue'), name: '401' }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
