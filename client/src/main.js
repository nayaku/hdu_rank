import Vue from 'vue'
import App from './App.vue'
import BootstrapVue from 'bootstrap-vue'
import './assets/css/index.css'
import './assets/css/font-awesome.min.css'
import axios from 'axios'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
let ajax = axios.create({
  baseURL: '/api/'
})
// 添加响应拦截器
ajax.interceptors.response.use(res => (res.data), error => {
  console.error(error)
  return Promise.reject(error)
})
Vue.prototype.$ajax = ajax
new Vue({
  render: h => h(App)
}).$mount('#app')
