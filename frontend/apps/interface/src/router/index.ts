import axios from 'axios'
import { route } from 'quasar/wrappers'
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory
} from 'vue-router'
import { StateInterface } from '../store'
import routes from './routes'
import { Loading, Notify } from 'quasar'
import { i18n } from '../boot/i18n'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route<StateInterface>(function ({ store }) {
  const createHistory =
    process.env.SERVER
      ? createMemoryHistory
      : process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE
    )
  })

  axios.defaults.withCredentials = true

  Router.beforeResolve((to, _from, next) => {
    // If this isn't an initial page load.
    if (to.name) {
      // Start the route progress bar.
      Loading.show({
        delay: 300 // ms
      })
    }
    next()
  })

  Router.afterEach(() => {
    // Complete the animation of the route progress bar.
    Loading.hide()
  })

  Router.beforeEach(async (to, _, next) => {
    store.commit('SET_API', 'http://' + window.location.hostname + ':9090')
    if (!store.getters.isAuthenticated && sessionStorage.getItem('learners-block-token') !== null) {
      await store.dispatch('VERIFY_LOGIN', sessionStorage.getItem('learners-block-token'))
    }
    if ((to.name === 'settings' || to.name === 'password_reset') && !store.getters.isAuthenticated) {
      await store.dispatch('LOGIN', { username: 'lb', password: ' ' }).catch(() => {
        next('/login')
      })
    }
    next()
  })

  axios.interceptors.response.use(function (response) {
    return response
  }, function (error) {
    if (error.response) {
      if (error.response.status === 401 || error.response.status === 422) {
        store.dispatch('LOGOUT')
        Router.push('/login')
        Notify.create({ type: 'negative', message: i18n.global.t('login_again') })
      }
    }
    return Promise.reject(error)
  })

  return Router
})
