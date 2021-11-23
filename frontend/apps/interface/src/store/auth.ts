import Axios from 'axios'
import { AxiosOverride } from 'src/boot/axios'

export interface AuthStateInterface {
  api: string,
  token: string
}
const auth = {
  state: <AuthStateInterface>{
    api: '',
    token: ''
  },
  getters: {
    isAuthenticated: (state: AuthStateInterface) => {
      return state.token !== '' && sessionStorage.getItem('learners-block-token') !== null
    },
    GET_API: (state: AuthStateInterface) => {
      return state.api
    }
  },
  mutations: {
    SET_TOKEN: (state: AuthStateInterface, payload: string) => {
      state.token = payload
    },
    SET_API: (state: AuthStateInterface, payload: string) => {
      state.api = ((process.env.DEV as unknown) as boolean) === true ? process.env.API as string : payload
    }
  },
  actions: {
    LOGIN: async ({ commit, getters }: { commit: any, getters: any }, payload: { username: string, password: string }) => {
      const response = await AxiosOverride.post(`${getters.GET_API}/v1/auth/log_in`, payload).catch(() => {
        throw Error('Wrong credentials')
      })
      if (response.status === 200) {
        const token = response.data.token
        sessionStorage.setItem('learners-block-token', token)
        Axios.defaults.headers.common.Authorization = `Bearer ${token}`
        AxiosOverride.defaults.headers.common.Authorization = `Bearer ${token}`
        commit('SET_TOKEN', token)
        return true
      }
    },
    LOGOUT: async ({ commit, getters }: { commit: any, getters: any }) => {
      const response = await Axios.post(`${getters.GET_API}/v1/auth/log_out`).catch(e => {
        throw new Error(e.message)
      })
      if (response.status === 200) {
        sessionStorage.removeItem('learners-block-token')
        Axios.defaults.headers.common.Authorization = ''
        AxiosOverride.defaults.headers.common.Authorization = ''
        commit('SET_TOKEN', null)
      }
    },
    VERIFY_LOGIN: async ({ commit, getters, dispatch }: { commit: any, getters: any, dispatch: any }, payload: string) => {
      const response = await Axios.get(`${getters.GET_API}/v1/auth/verify_login`, {
        headers: {
          Authorization: `Bearer ${payload}`
        }
      })
      if (response.data.logged_in === true) {
        commit('SET_TOKEN', payload)
        Axios.defaults.headers.common.Authorization = `Bearer ${payload}`
        AxiosOverride.defaults.headers.common.Authorization = `Bearer ${payload}`
      } else {
        dispatch('LOGOUT')
      }
    }
  }
}
export default auth
