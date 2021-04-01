import axios from 'axios'
import { route } from 'quasar/wrappers'
import routes from './routes'
import { Store } from 'vuex'
import store, { StateInterface } from '../store'
import VueRouter from 'vue-router'
import { Loading } from 'quasar'
/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation
 */

export default route<Store<StateInterface>>(function ({ Vue }) {
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

  Router.beforeResolve((to, _from, next) => {
    // If this isn't an initial page load.
    if (to.name) {
      // Start the route progress bar.
      Loading.show({
        delay: 400 // ms
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
      store.dispatch('LOGIN', { username: 'lb', password: ' ' }).then(() => {
        next()
      }).catch(() => {
        next('/login')
      }).catch(() => {
        next()
      })
    } else if (to.name === 'login' && store.getters.isAuthenticated) {
      next('/')
    } else {
      next()
    }
  })
  axios.interceptors.response.use(function (response) {
    return response
  }, function (error) {
    if (error.resonse) {
      if (error.response.status === 401 || error.code === 'ECONNABORTED') {
        store.dispatch('LOGOUT')
        if (Router.currentRoute.fullPath !== '/') {
          Router.push('/login')
        }
      } else {
        console.log(error.response.status)
        Router.push('/' + error.response.status)
      }
    }
    return Promise.reject(error)
  })

  return Router
})
