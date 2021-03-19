/* eslint-disable @typescript-eslint/no-explicit-any */
import Axios from 'axios'

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
      return state.token !== '' && localStorage.getItem('learners-block-token') !== null
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
      const response = await Axios.post(`${getters.GET_API}/v1/login`, payload).catch(() => {
        throw Error('Wrong credentials')
      })
      if (response.status === 200) {
        const token = response.data.token
        localStorage.setItem('learners-block-token', token)
        Axios.defaults.headers.common.Authorization = `Bearer ${token}`
        commit('SET_TOKEN', token)
        return true
      }
    },
    LOGOUT: async ({ commit, getters }: { commit: any, getters: any }) => {
      const response = await Axios.post(`${getters.GET_API}/v1/logout`).catch(e => {
        throw new Error(e.message)
      })
      if (response.status === 200) {
        localStorage.removeItem('learners-block-token')
        Axios.defaults.headers.common.Authorization = null
        commit('SET_TOKEN', null)
      }
    },
    VERIFY_LOGIN: async ({ commit, getters }: { commit: any, getters: any }, payload: string) => {
      const response = await Axios.get(`${getters.GET_API}/v1/verifylogin`, {
        headers: {
          Authorization: `Bearer ${payload}`
        }
      })
      if (response.data.logged_in === true) {
        commit('SET_TOKEN', payload)
        Axios.defaults.headers.common.Authorization = `Bearer ${payload}`
      }
    }
  }
}
export default auth
