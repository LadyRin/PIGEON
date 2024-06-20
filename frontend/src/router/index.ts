import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/LoginView.vue'
import EventList from '@/views/EventListView.vue'
import AddEvent from '@/views/AddEventView.vue'
import Admin from '@/views/AdminView.vue'

import { useAuthStore } from '@/core/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/',
      alias: '/events',
      name: 'EventList',
      component: EventList,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/events/new',
      name: 'AddEvent',
      component: AddEvent,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/events/edit/:id',
      name: 'EditEvent',
      component: AddEvent,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin,
      meta: {
        requiresAuth: true,
        requiresAdmin: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = useAuthStore().isAuthenticated
  const isAdmin = useAuthStore().isAdmin
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
