import { route } from 'quasar/wrappers'
import VueRouter from 'vue-router'
import { Store } from 'vuex'
import store, { StateInterface } from '../store'

import routes from './routes'
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

  Router.beforeEach(async (to, _, next) => {
    store.commit('SET_API', window.location.origin + ':9090')
    if (!store.getters.isAuthenticated && localStorage.getItem('learners-block-token') !== null) {
      await store.dispatch('VERIFY_LOGIN', localStorage.getItem('learners-block-token'))
    }
    if ((to.name === 'settings' || to.name === 'password_reset') && !store.getters.isAuthenticated) {
      store.dispatch('LOGIN', { username: 'lb', password: ' ' }).then(() => {
        next()
      }).catch(() => {
        next('/login')
      })
    } else if (to.name === 'login' && store.getters.isAuthenticated) {
      next('/')
    } else {
      next()
    }
  })

  return Router
})
