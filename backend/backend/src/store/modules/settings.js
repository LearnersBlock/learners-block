import Api from '@/api/Api'
import get from 'lodash/get'
import set from 'lodash/set'

export default {
    namespaced: true,
    state: {
        loading: true,
        settings: null
    },

    /*
     * Mutations
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /*
         * SET_SETTINGS
         */
        SET_SETTINGS (state, data) {
            state.settings = data.data
        },

        /*
         * UPDATE_SETTINGS
         */
        UPDATE_SETTING (state, data) {
            set(state.settings, `${data.group}.${data.key}`, data.value)
        },

        /*
         * SET_LOADING_STATE
         */
        SET_LOADING_STATE (state, status) {
            state.loading = status
        }
    },

    /*
     * Getters
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        /*
         * getSettings
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

    /*
     * Actions
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {
        /*
         * fetchSettings
         */
        fetchSettings (context, params) {
            if (!context.state.settings) {
                return Api().get('/settings')
                    .then(r => r.data)
                    .then(response => {
                        context.commit('SET_SETTINGS', response)
                        context.commit('SET_LOADING_STATE', false)
                    })
            }
        },

        /*
         * update
         */
        update (context, params) {
            // enable loading state
            context.commit('SET_LOADING_STATE', true)

            // get current state as backup (see expl. below)
            const originalState = context.getters.getSettingFromPath(`${params.group}.${params.key}`)

            // commit new value
            // this is being done here for improved UX – if the commit would
            // only be triggered after successful API call, the toggle switch
            // would be delayed
            context.commit('UPDATE_SETTING', params)

            // trigger the API call
            return new Promise((resolve, reject) => {
                Api().patch('/settings', params)
                    .then((response) => {
                        setTimeout(() => {
                            // disable loading state
                            context.commit('SET_LOADING_STATE', false)

                            // resolve promise
                            resolve(response)
                        }, 1400)
                    })
                    .catch(err => {
                        setTimeout(() => {
                            // reset state to original state
                            params.value = originalState
                            context.commit('UPDATE_SETTING', params)

                            // disable loading state
                            context.commit('SET_LOADING_STATE', false)

                            // reject promise
                            reject(err)
                        }, 600)
                    })
            })
        }
    }
}
