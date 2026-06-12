import { createRouter, createWebHistory } from 'vue-router'
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

export default router
