import axios from 'axios'
import { route } from 'quasar/wrappers'
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory
} from 'vue-router'
import { SessionStorage } from 'quasar'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory =
    process.env.SERVER
      ? createMemoryHistory
      : process.env.VUE_ROUTER_MODE === 'history'
        ? createWebHistory
        : createWebHashHistory

  const Router = createRouter({
    scrollBehavior (_to, _from, savedPosition) {
      if (savedPosition) {
        return savedPosition
      } else {
        return { top: 0 }
      }
    },
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(
      // eslint-disable-next-line no-void
      process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE
    )
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
      if (error.response.status === 401 || error.response.status === 421) {
        location.href = '/settings/'
      }
    }
  })

  return Router
})
