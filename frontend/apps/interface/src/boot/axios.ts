import { boot } from 'quasar/wrappers'
import axios, { AxiosInstance } from 'axios'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance
  }
}

// Override function to skip interceptors
const AxiosOverride = axios.create()

export default boot(({ app }) => {
  app.config.globalProperties.$axios = axios
})

export { axios, AxiosOverride }
