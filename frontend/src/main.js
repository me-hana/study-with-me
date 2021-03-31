import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';
import routes from './routes';
import store from './vuex/store';
import vuetify from './plugins/vuetify';
import VueFullPage from 'vue-fullpage.js';
import Carousel3d from 'vue-carousel-3d';

Vue.config.productionTip = false;

Vue.use(VueRouter);
Vue.use(VueFullPage);
Vue.use(Carousel3d);

const router = new VueRouter({
  mode: 'history',
  routes,
});

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
