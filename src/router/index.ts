import axios from 'axios'
import { route } from 'quasar/wrappers'
import VueRouter from 'vue-router'
import routes from './routes'
import { SessionStorage } from 'quasar'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation
 */

export default route(function ({ Vue }) {
  Vue.use(VueRouter)

  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,

    // Leave these as is and change from quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  })

  axios.defaults.withCredentials = true

  try {
    const token = SessionStorage.getItem('learners-block-token')
    axios.defaults.headers.common.Authorization = `Bearer ${token}`
  } catch (e) {
    location.href = '/settings/'
  }

  axios.interceptors.response.use(function (response) {
    return response
  }, function (error) {
    if (error.response) {
      if (error.response.status === 401 || error.response.status === 421 || error.code === 'ECONNABORTED') {
        location.href = '/settings/'
      }
    }
  })

  return Router
})
