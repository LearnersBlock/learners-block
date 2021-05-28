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
      { path: '/captive_portal', component: () => import('pages/CaptivePortal.vue'), name: 'captive_portal' },
      { path: '/upload_makerspace', component: () => import('pages/UploadMakerSpace.vue'), name: 'upload_makerspace' },
      { path: '/epub_reader', component: () => import('pages/Epub.vue'), name: 'epub_reader' },
      { path: '/portainer', redirect: '/portainer//' },
      // route to fix invalid router replace when clicking password reset from /settings/ page ratner than /settings
      { path: '/settings/password_reset', redirect: '/password_reset' },
      { path: '/401', component: () => import('pages/401.vue'), name: '401' }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
