import i18n from '../../i18n'
import Cookies from 'js-cookie'

const langCookieName = 'lb__lang'

export default {
    namespaced: true,
    state: {
        default: null,
        current: null
    },

    /**
     * Mutations
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /**
         * Set the current locale
         *
         * @param   {Object} state The vuex state
         * @param   {String} lang The locale to store
         * @returns void
         */
        SET_CURRENT_LANG (state, lang) {
            state.current = lang
        }
    },

    /**
     * Getters
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        /**
         * Get the list of available locales
         *
         * @param   {Object} state The vuex state
         * @returns void
         */
        availableLocales: (state) => {
            return i18n.availableLocales
        }
    },

    /**
     * Actions
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {
        /**
         * Update the prefered locale
         *
         * @param   {Object}    context The vuex context
         * @param   {Object}    params The update request params
         * @returns {Object}    void
         */
        updateLang (context, params) {
            // Get the list of available locales
            const availableLocales = context.getters.availableLocales

            // If we have available locales and the value stored in the cookies
            // is present in that list
            if (availableLocales && availableLocales.includes(params.lang)) {
                // Set the lang to the user preferences stored in the cookie
                i18n.locale = params.lang

                // Update store
                context.commit('SET_CURRENT_LANG', params.lang)

                // Check if the new lang locale is to be stored
                if (params.store) {
                    // Store that preference
                    Cookies.set(langCookieName, params.lang)
                }
            } else {
                // Otherwise, remove the cookie as the stored language is not an
                // acceptable parameter
                Cookies.remove(langCookieName)

                // Update store
                context.commit('SET_CURRENT_LANG', i18n.locale)

                // Emit error
                // console.error('[store/lang/updateLang]', `The passed language parameter "${params.lang}" is not available`)
            }
        }
    }
}
