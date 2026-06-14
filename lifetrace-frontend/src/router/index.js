import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import HealthWeatherView from '../views/HealthWeatherView.vue'
import ScheduleView from '../views/ScheduleView.vue'
import AiAssistantView from '../views/AiAssistantView.vue'
import ProductView from '../views/ProductView.vue'
import QueueView from '../views/QueueView.vue'

const routes = [
  {
    path: '/',
    redirect: '/health',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      public: true,
      hideNav: true,
    },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      public: true,
      hideNav: true,
    },
  },
  {
    path: '/health',
    name: 'health',
    component: HealthWeatherView,
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: ScheduleView,
  },
  {
    path: '/ai',
    name: 'ai',
    component: AiAssistantView,
  },
  {
    path: '/products',
    name: 'products',
    component: ProductView,
  },
  {
    path: '/queue',
    name: 'queue',
    component: QueueView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()

  if (to.meta.public && isAuthenticated.value) {
    return '/health'
  }

  if (!to.meta.public && !isAuthenticated.value) {
    return {
      path: '/login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  return true
})

export default router
