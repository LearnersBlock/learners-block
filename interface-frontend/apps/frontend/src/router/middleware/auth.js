import store from '../../store'

export async function IsAuthenticated (to, from, next) {
    try {
        await Promise.all([
            // force fetch the auth requirements to make sure the vuex state is
            // always up to date and weren't change mid-session
            store.dispatch('auth/getAuthRequirements')
        ]).then(() => {
            // check if auth has been enabled
            if (store.getters['auth/isAuthRequired'] === true) {
                // if so, check if the user is currently logged in
                if (store.getters['auth/isAuthenticated']) {
                    // if so, proceed
                    next()
                } else {
                    // otherwise, head to login
                    next(`/login?redirect=${to.path}`)
                }
            } else if (store.getters['auth/isAuthRequired'] === false) {
                // otherwise, proceed without login
                next()

                // emit console warning
                // console.warn(`[router/middleware/auth] Auth has not been enabled, accessing ${to.name} (${to.path}) without authentication`)
            } else {
                // otherwise, emit error as isAuthRequired didn't return a valid
                // response and shouldn't allow login at this stage
                next('/500')

                // emit console error
                // console.error('[router/middleware/auth]', 'Auth requirements could not be fetched')
            }
        })
    } catch (error) {
        // emit error
        next('/500')
        // console.error('[router/middleware/auth]', 'Auth requirements could not be fetched')
    }
}

export function IsNotAuthenticated (to, from, next) {
    // check if the session is authenticated
    if (!store.getters['auth/isAuthenticated']) {
        // if thise isn't the case, proceed (i.e. login)
        next()
    } else {
        // otherwise, redirect as there is no need to be here
        // check if we have the redirect param
        if (to.query.redirect) {
            // if so, head there
            next(to.query.redirect)
        } else {
            // otherwise, head home
            next('/')
        }
    }
}

export default { IsAuthenticated, IsNotAuthenticated }
