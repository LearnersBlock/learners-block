export default {
    namespaced: true,
    state: {
        loading: false
    },

    /*
     * Mutations
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /*
         * SET_LOADING
         */
        SET_LOADING (state, response) {
            state.loading = response
        }
    },

    /*
     * Getters
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        isLoading: state => state.loading
    },

    /*
     * Actions
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {}
}
