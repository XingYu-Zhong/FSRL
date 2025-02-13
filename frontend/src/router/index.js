import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '/',
        redirect: '/dashboard'
      },
      {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue')
      },
      {
        path: '/training',
        name: 'Training',
        component: () => import('../views/Training.vue')
      },
      {
        path: '/configs',
        name: 'Configs',
        component: () => import('../views/Configs.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 