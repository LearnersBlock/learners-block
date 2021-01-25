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

    /**
     * Mutations
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /**
         * Set logged-in state by storing auth parameters
         */
        AUTH_LOGIN (state, response) {
            if (response.data.success) {
                // Get token
                const token = response.data.data.token
                const permissions = response.data.data.permissions
                const username = response.data.data.username

                // Update store status
                state.username = username
                state.token = token
                state.permissions = permissions

                // Store in cookie
                Cookies.set(authCookieName, JSON.stringify({
                    token,
                    permissions,
                    username
                }))
            }
        },

        /**
         * Set logged-out state by removing all stored auth parameters
         */
        AUTH_LOGOUT (state, response) {
            // Update store
            state.token = null
            state.permissions = null
            state.username = null

            // Update session cookie
            Cookies.remove(authCookieName)
        },

        /**
         * Update the auth requirements
         */
        AUTH_REQUIRED (state, response) {
            // Update store
            state.required = response
        },

        /**
         * Update the loading state
         */
        AUTH_REQUEST (state, status) {
            // Update store
            state.loading = status
        },

        /**
         * Store an auth error
         */
        AUTH_ERROR (state) {
            // Update store
            state.status = 'error'
        }
    },

    /**
     * Getters
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        isAuthenticated: state => !!state.token,
        hasAdminPermissions: state => state.permissions === 'admin',
        hasTeacherPermissions: state => state.permissions === 'teacher',
        isAuthLoading: state => state.loading,
        isAuthRequired: state => state.required
    },

    /**
     * Actions
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {
        /**
         * Get the auth requirements (whether auth is enabled or not)
         *
         * @param {Object}      context The vuex context
         * @param {Object}      params The auth request params
         * @returns {Object}    The API response
         */

        getAuthRequirements (context, params) {
            // Enable loading state
            context.commit('AUTH_REQUEST', true)

            // Run API request
            return new Promise((resolve, reject) => {
                Api().get('/auth/check', params)
                    .then((response) => {
                        // Run commit
                        context.commit('AUTH_REQUIRED', response.data.data.enabled)

                        // Disable loading state
                        context.commit('AUTH_REQUEST', false)

                        // Resolve promise with the request response
                        resolve(response)
                    })
                    .catch(err => {
                        setTimeout(() => {
                            // Set error
                            context.commit('AUTH_ERROR', err)

                            // Disable loading state
                            context.commit('AUTH_REQUEST', false)

                            // Reject promise with error
                            reject(err)
                        }, 600)
                    })
            })
        },

        /**
         * Login
         *
         * @param {Object}      context The vuex context
         * @param {Object}      params The login request params
         * @returns {Object}    The API response
         */
        login (context, params) {
            // Enable loading state
            context.commit('AUTH_REQUEST', true)

            // Run API request
            return new Promise((resolve, reject) => {
                Api().post('/auth/login', params)
                    .then((response) => {
                        setTimeout(() => {
                            // Run login commit
                            context.commit('AUTH_LOGIN', response)

                            // Disable loading state
                            context.commit('AUTH_REQUEST', false)

                            // Resolve promise with API response
                            resolve(response)
                        }, 1400)
                    })
                    .catch(err => {
                        setTimeout(() => {
                            // Set error
                            context.commit('AUTH_ERROR', err)

                            // Since the request failed, remove any possible auth token
                            Cookies.remove(authCookieName)

                            // Disable loading state
                            context.commit('AUTH_REQUEST', false)

                            // Reject promise with API response
                            reject(err)
                        }, 600)
                    })
            })
        },

        /**
         * Logout
         *
         * @param {Object}      context The vuex context
         * @param {Object}      params The logout request params
         * @returns {Object}    The API response
         */
        logout (context, params) {
            // Enable loading state
            context.commit('AUTH_REQUEST', true)

            // Logout
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
