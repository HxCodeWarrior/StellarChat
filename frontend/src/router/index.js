import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import ChatView from '@/views/ChatView.vue'
import GetApiKey from '@/views/GetApiKey.vue'
import ApiKeyManagement from '@/views/ApiKeyManagement.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView,
    },
    {
      path: '/get-api-key',
      name: 'get-api-key',
      component: GetApiKey,
    },
    {
      path: '/api-key-management',
      name: 'api-key-management',
      component: ApiKeyManagement,
    },
  ],
})

export default router
