// frontend/src/router/index.js
// Configuration des routes (navigation entre pages)

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DatasetDetail from '../views/DatasetDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      // Route dynamique : ":id" est un paramètre
      // Ex: /datasets/ODP846 → DatasetDetail avec route.params.id = "ODP846"
      path: '/datasets/:id',
      name: 'dataset-detail',
      component: DatasetDetail
    },
  ]
})

export default router