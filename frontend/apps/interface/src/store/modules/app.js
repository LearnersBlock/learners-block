export default {
    namespaced: true,
    state: {
        loading: false
    },

    /**
     * Mutations
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /***
         * Update loading state
         */
        SET_LOADING (state, response) {
            state.loading = response
        }
    },

    /**
     * Getters
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        /**
         * Get loading state
         */
        isLoading: state => state.loading
    },

    /**
     * Actions
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {}
}
