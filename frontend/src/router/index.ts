import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/DashboardView.vue'
import Login from '@/views/LoginView.vue'
import { useAuthStore } from '@/core/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        requiresAuth: false
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = useAuthStore().isAuthenticated
  console.log(isAuthenticated)
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
