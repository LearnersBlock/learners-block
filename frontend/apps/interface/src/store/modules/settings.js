import Api from '@/api/Api'
import get from 'lodash/get'
import set from 'lodash/set'

export default {
    namespaced: true,
    state: {
        loading: true,
        settings: null
    },

    /**
     * Mutations
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /**
         * Set the settings data
         *
         * @param   {Object} state The vuex state
         * @param   {Object} data Settings to set
         * @returns void
         */
        SET_SETTINGS (state, data) {
            state.settings = data.data
        },

        /**
         * Update a setting
         *
         * @param   {Object} state The vuex state
         * @param   {Object} data Set of settings data to update
         * @returns void
         */
        UPDATE_SETTING (state, data) {
            set(state.settings, `${data.group}.${data.key}`, data.value)
        },

        /**
         * Update loading state
         *
         * @param   {Object} state The vuex state
         * @param   {Boolean} status Whether or not we're loading
         * @returns void
         */
        SET_LOADING_STATE (state, status) {
            state.loading = status
        }
    },

    /**
     * Getters
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        /*
         * Get the complete set of settings
         */

        getSettings: (state) => {
            return state.settings
        },

        /*
         * getSettingFromPath
         */

        getSettingFromPath: (state) => {
            return (path) => {
                return get(state.settings, path)
            }
        }
    },

    /**
     * Actions
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {
        /**
         * Fetch the settings
         *
         * @param   {Object}    context The vuex context
         * @returns {Object}    void
         */
        fetchSettings (context) {
            // Check if settings have already been fetched
            if (!context.state.settings) {
                // If not, trigger API request
                return Api().get('/settings')
                    .then(r => r.data)
                    .then(response => {
                        context.commit('SET_SETTINGS', response)
                        context.commit('SET_LOADING_STATE', false)
                    })
            }
        },

        /**
         * Update setting
         *
         * @param   {Object}    context The vuex context
         * @param   {Object}    params The update request params
         * @returns {Object}    void
         */
        update (context, params) {
            // Enable loading state
            context.commit('SET_LOADING_STATE', true)

            // Get current state as backup (see expl. below)
            const originalState = context.getters.getSettingFromPath(`${params.group}.${params.key}`)

            // Commit new value
            // This is being done here for improved UX – if the commit would
            // only be triggered after successful API call, the toggle switch
            // would be delayed
            context.commit('UPDATE_SETTING', params)

            // Trigger the API call
            return new Promise((resolve, reject) => {
                Api().patch('/settings', params)
                    .then((response) => {
                        setTimeout(() => {
                            // Disable loading state
                            context.commit('SET_LOADING_STATE', false)

                            // Resolve promise
                            resolve(response)
                        }, 1400)
                    })
                    .catch(err => {
                        setTimeout(() => {
                            // Reset state to original state
                            params.value = originalState
                            context.commit('UPDATE_SETTING', params)

                            // Disable loading state
                            context.commit('SET_LOADING_STATE', false)

                            // Reject promise
                            reject(err)
                        }, 600)
                    })
            })
        }
    }
}
