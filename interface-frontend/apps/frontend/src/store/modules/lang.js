// import Api from '@/api/Api'
import i18n from '../../i18n'
import Cookies from 'js-cookie'

const langCookieName = 'lb__lang'

export default {
    namespaced: true,
    state: {
        default: null,
        current: null
    },

    /*
     * Mutations
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    mutations: {
        /*
         * SET_CURRENT_LANG
         */
        SET_CURRENT_LANG (state, lang) {
            state.current = lang
        }
    },

    /*
     * Getters
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    getters: {
        /*
         * availableLocales
         */

        availableLocales: (state) => {
            return i18n.availableLocales
        }
    },

    /*
     * Actions
     *
     * @since           0.0.1
     * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

    actions: {
        /*
         * updateLang
         */
        updateLang (context, params) {
            // get the list of available locales
            const availableLocales = context.getters.availableLocales

            // if we have available locales and the value stored in the cookies is
            // present in that list
            if (availableLocales && availableLocales.includes(params.lang)) {
                // set the lang to the user preferences stored in the cookie
                i18n.locale = params.lang

                // update store
                context.commit('SET_CURRENT_LANG', params.lang)

                // check if the new lang locale is to be stored
                if (params.store) {
                    // store that preference
                    Cookies.set(langCookieName, params.lang)
                }
            } else {
                // otherwise, remove the cookie as the stored language is not an
                // acceptable parameter
                Cookies.remove(langCookieName)

                // update store
                context.commit('SET_CURRENT_LANG', i18n.locale)

                // emit error
                // console.error('[store/lang/updateLang]', `The passed language parameter "${params.lang}" is not available`)
            }
        }
    }
}
