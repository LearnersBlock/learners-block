import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Home.vue'), name: 'home' },
      {
        path: '/captive_portal',
        component: () => import('pages/CaptivePortal.vue'),
        name: 'captive_portal'
      },
      {
        path: '/epub_reader',
        component: () => import('pages/Epub.vue'),
        name: 'epub_reader'
      },
      {
        path: '/filemanager',
        component: () => import('pages/FileManager.vue'),
        name: 'filemanager'
      },
      {
        path: '/library',
        component: () => import('pages/library/Library.vue'),
        name: 'library'
      },
      {
        path: '/library/resource/:id',
        component: () => import('pages/library/Resource.vue'),
        name: 'library_resource'
      },
      {
        path: '/login',
        component: () => import('pages/Login.vue'),
        name: 'login'
      },
      {
        path: '/settings',
        component: () => import('pages/Settings.vue'),
        name: 'settings'
      },
      {
        path: '/wifi',
        component: () => import('pages/WifiConnect.vue'),
        name: 'wifi'
      },
      { path: '/401', component: () => import('pages/401.vue'), name: '401' }
    ]
  },
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
