import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/Ping.vue';
import Translator from '../components/Translator.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Translator',
      component: Translator,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
