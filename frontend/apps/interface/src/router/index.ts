import axios, {
  AxiosRequestConfig
} from 'axios'
import { i18n } from '../boot/i18n'
import { Loading, Notify } from 'quasar'
import { route } from 'quasar/wrappers'
import routes from './routes'
import { AxiosOverride } from 'src/boot/axios'
import { StateInterface } from '../store'
import { ref } from 'vue'
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory
} from 'vue-router'

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
    scrollBehavior (_to, _from, savedPosition) {
      if (savedPosition) {
        return savedPosition
      } else {
        return { left: 0, top: 0 }
      }
    },
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE
    )
  })

  function notifyError (message) {
    Notify.create({
      type: 'negative',
      message: message,
      timeout: 0,
      actions: [
        {
          label: `${i18n.global.t('close')}`,
          color: 'white',
          handler: () => { /* ... */ }
        }
      ]
    })
  }

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
    // Set the API string on each request for use throughout the app
    store.commit('SET_API', 'http://' + window.location.hostname + ':9090')
    // If there is a token stored but user is not logged in, re-validate it
    if (!store.getters.isAuthenticated && sessionStorage.getItem('learners-block-token') !== null) {
      await store.dispatch('VERIFY_LOGIN', sessionStorage.getItem('learners-block-token'))
    }
    // If protected route
    if ((to.name === 'settings' || to.name === 'wifi') && !store.getters.isAuthenticated) {
      // Try logging in without a password, and if error then redirect to login page
      await store.dispatch('LOGIN', { username: 'lb', password: ' ' }).catch(() => {
        void Router.replace({ name: 'login', params: { data: to.fullPath } })
      })
    }
    // If login successful, allow access.
    next()
  })

  axios.interceptors.response.use(function (response) {
    return response
  }, async function (error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx

      // If an auth related error
      if (error.response.status === 401 || error.response.status === 422) {
        const overrideResponse = ref<any>()
        // Try logging in again in case of a token timeout and no password set
        await store.dispatch('LOGIN', { username: 'lb', password: ' ' }).then(async () => {
          const originalRequestConfig = error.config
          // Remove old token to force use of new one
          delete originalRequestConfig.headers.Authorization
          // Retry request with new Auth header
          overrideResponse.value = await AxiosOverride(originalRequestConfig as AxiosRequestConfig<any>).catch(() => {
            // Should be no reason to reach this error
            notifyError(i18n.global.t('error'))
          })
        }).catch(() => {
          // If unable to login with default username and password
          void Router.replace({ name: 'login', params: { data: Router.currentRoute.value.fullPath } })
          Notify.create({
            type: 'negative',
            message: i18n.global.t('login_again'),
            timeout: 1500
          })
        })
        // If a successful response, return promise
        if (overrideResponse.value) {
          return Promise.resolve(overrideResponse.value)
        } else {
          // If all error captures fail, return a rejected promise
          return Promise.reject(error)
        }
      // If a non-auth related error code, report an error
      } else {
        console.log(error.response)
        if (error.response.data.message) {
          notifyError(`${i18n.global.t('error')} ${error.response.data.message}`)
        } else {
          notifyError(`${i18n.global.t('error')} ${error.response.statusText}`)
        }
      }
      return Promise.reject(error)
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
      // http.ClientRequest in node.js
      console.log(error.request)
      notifyError(`${i18n.global.t('error')}`)
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message)
      notifyError(`${i18n.global.t('error')} ${error.message}`)
    }
  })
  return Router
})
