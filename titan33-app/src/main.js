import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import CapitalCurve from './components/CapitalCurve.vue';
import TrainingResults from './components/TrainingResults.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/capital-curve', component: CapitalCurve },
    { path: '/training-results', component: TrainingResults }
  ]
});

createApp(App).use(router).mount('#app');