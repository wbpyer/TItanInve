import { createRouter, createWebHistory } from 'vue-router';
import StockSelector from '../views/StockSelector.vue';
import AlgorithmSelector from '../views/AlgorithmSelector.vue'; // 你将在后面创建这个组件

const routes = [
  { path: '/', component: StockSelector },
  { path: '/result', component: AlgorithmSelector },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;