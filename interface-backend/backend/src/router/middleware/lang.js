import store from '../../store'
import Cookies from 'js-cookie'

const langCookieName = 'lb__lang'

export function getLangState (to, from, next) {
    return store.state.lang.current || false
}

export async function setLang (to, from, next) {
    // attempt to get the language cookie data
    const storedLang = Cookies.get(langCookieName)

    // if the cookie returned a result
    if (storedLang) {
        // run the lang update
        // this either updates the current locale or removes the cookie if the
        // lang isn't actually present in the list of available locales
        store.dispatch('lang/updateLang', { lang: storedLang, store: true })
    } else {
        // no user preferences were stored in the cookies
        // now, check if the default language was set by an app admin
        let defaultLang = store.getters['settings/getSettingFromPath']('lang.default')

        if (defaultLang) {
            // run the lang update
            store.dispatch('lang/updateLang', { lang: defaultLang, store: false })
        } else {
            // otherwise, fetch the settings from the backend
            try {
                await Promise.all([
                    store.dispatch('settings/fetchSettings')
                ]).then(() => {
                    // try to access the settings again
                    defaultLang = store.getters['settings/getSettingFromPath']('lang.default')

                    // check if we have the default language parameter
                    if (defaultLang) {
                        // run the lang update
                        store.dispatch('lang/updateLang', { lang: defaultLang, store: false })
                    }
                })
            } catch (error) {
                // emit error
                console.error('[router/middleware/setLang]', 'Settings could not be fetched')  // eslint-disable-line
            }
        }
    }

    next()
}

export default { setLang, getLangState }
