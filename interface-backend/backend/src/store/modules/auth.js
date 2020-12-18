import Api from '@/api/Api'
import Cookies from 'js-cookie'

const authCookieName = 'lb__auth'

const storage = Cookies.get(authCookieName) ? JSON.parse(Cookies.get(authCookieName)) : null

export default {
    namespaced: true,
    state: {
        loading: false,
        required: false,
        username: storage ? storage.username : '',
        token: storage ? storage.token : '',
        permissions: storage ? storage.permissions : ''
    },

    /*
     * Mutations
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /*
         * SET_LOGIN
         */
        AUTH_LOGIN (state, response) {
            if (response.data.success) {
                // get token
                const token = response.data.data.token
                const permissions = response.data.data.permissions
                const username = response.data.data.username

                // update store status
                state.username = username
                state.token = token
                state.permissions = permissions

                // store in cookie
                Cookies.set(authCookieName, JSON.stringify({
                    token,
                    permissions,
                    username
                }))
            }
        },

        /*
         * SET_LOGOUT
         */
        AUTH_LOGOUT (state, response) {
            // update store
            state.token = null
            state.permissions = null
            state.username = null

            // update session cookie
            Cookies.remove(authCookieName)
        },

        AUTH_REQUIRED (state, response) {
            // update store
            state.required = response
        },

        AUTH_REQUEST (state, status) {
            state.loading = status
        },

        AUTH_ERROR (state) {
            state.status = 'error'
        }
    },

    /*
     * Getters
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        isAuthenticated: state => !!state.token,
        hasAdminPermissions: state => state.permissions === 'admin',
        hasTeacherPermissions: state => state.permissions === 'teacher',
        isAuthLoading: state => state.loading,
        isAuthRequired: state => state.required
    },

    /*
     * Actions
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {
        /*
         * getAuthRequirements
         */
        getAuthRequirements (context, params) {
            // enable loading state
            context.commit('AUTH_REQUEST', true)

            return new Promise((resolve, reject) => {
                Api().get('/auth/check', params)
                    .then((response) => {
                        // run commit
                        context.commit('AUTH_REQUIRED', response.data.data.enabled)

                        // disable loading state
                        context.commit('AUTH_REQUEST', false)

                        // resolve promise
                        resolve(response)
                    })
                    .catch(err => {
                        setTimeout(() => {
                            context.commit('AUTH_ERROR', err)

                            // disable loading state
                            context.commit('AUTH_REQUEST', false)

                            // reject promise
                            reject(err)
                        }, 600)
                    })
            })
        },

        /*
         * login
         */
        login (context, params) {
            // enable loading state
            context.commit('AUTH_REQUEST', true)

            return new Promise((resolve, reject) => {
                Api().post('/auth/login', params)
                    .then((response) => {
                        setTimeout(() => {
                            // run login commit
                            context.commit('AUTH_LOGIN', response)

                            // disable loading state
                            context.commit('AUTH_REQUEST', false)

                            // add access token to axios
                            // axios.defaults.headers.common.Authorization = token

                            // resolve promise
                            resolve(response)
                        }, 1400)
                    })
                    .catch(err => {
                        setTimeout(() => {
                            context.commit('AUTH_ERROR', err)

                            // if the request fails, remove any possible auth token
                            Cookies.remove(authCookieName)

                            // disable loading state
                            context.commit('AUTH_REQUEST', false)

                            // reject promise
                            reject(err)
                        }, 600)
                    })
            })
        },

        /*
         * login
         */
        logout (context, params) {
            context.commit('AUTH_REQUEST', true)

            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    context.commit('AUTH_LOGOUT')
                    context.commit('AUTH_REQUEST', false)
                    resolve()
                }, 1400)
            })
        }
    }
}
