import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import './assets/css/index.css'
import axios from 'axios'
import 'prismjs'
import 'prismjs/themes/prism.css'
import VuePrismEditor from 'vue-prism-editor'
import 'vue-prism-editor/dist/VuePrismEditor.css'
// import './assets/css/font-awesome.min.css'
// import 'bootstrap/dist/css/bootstrap.css'
// import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.config.productionTip = false

Vue.component('prism-editor', VuePrismEditor)
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
let ajax = axios.create({
  baseURL: (process && process.env.NODE_ENV === 'development') ? 'http://localhost:5000/api' : '/api/'
})
ajax.defaults.withCredentials = true
Vue.prototype.$ajax = ajax

new Vue({
  render: h => h(App)
}).$mount('#app')
