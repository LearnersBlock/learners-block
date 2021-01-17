import Vue from 'vue'
import VueRouter from 'vue-router'

// components
import Home from '../views/Home.vue'
import WifiPortal from '../views/WifiPortal.vue'
import Settings from '../views/Settings.vue'
import SettingsHome from '../views/Settings/Home.vue'
import SettingsComponents from '../views/Settings/Components.vue'
import SettingsLanguage from '../views/Settings/Language.vue'
import SettingsNetwork from '../views/Settings/Network.vue'
import SettingsUsers from '../views/Settings/Users.vue'
import SettingsSystem from '../views/Settings/System.vue'

// middlewares
import { IsNotAuthenticated, IsAuthenticated } from './middleware/auth'
import { setLang, getLangState } from './middleware/lang'

// init router
Vue.use(VueRouter)

// routes
const routes = [
    {
        path: '/',
        component: Home
    },
    {
        path: '/settings',
        beforeEnter: IsAuthenticated,
        component: Settings,
        children: [
            {
                path: '',
                component: SettingsHome
            },
            {
                path: '/settings/components',
                component: SettingsComponents,
                meta: { transitionName: 'slide' }
            },
            {
                path: '/settings/language',
                component: SettingsLanguage,
                meta: { transitionName: 'slide' }
            },
            {
                path: '/settings/network',
                component: SettingsNetwork,
                meta: { transitionName: 'slide' }
            },
            {
                path: '/settings/users',
                component: SettingsUsers,
                meta: { transitionName: 'slide' }
            },
            {
                path: '/settings/system',
                component: SettingsSystem,
                meta: { transitionName: 'slide' }
            }
        ]
    },
    {
        path: '/captive-portal',
        component: WifiPortal
    },
    {
        path: '/login',
        beforeEnter: IsNotAuthenticated,
        component: () => import(
            /* webpackChunkName: "auth.login" */ '../views/auth/Login.vue'
        )
    },
    {
        path: '/logout',
        component: () => import(
            /* webpackChunkName: "auth.logout" */ '../views/auth/Logout.vue'
        )
    },
    {
        path: '/404',
        component: () => import(
            /* webpackChunkName: "auth.login" */ '../views/Error.vue'
        )
    },
    {
        path: '/500',
        component: () => import(
            /* webpackChunkName: "auth.login" */ '../views/Error.vue'
        )
    },
    {
        path: '/files/admin',
        redirect: () => {
            // redirect to the filemanager path
            window.location.href = '/files?mode=admin'
        }
    }
]

const router = new VueRouter({
    routes
})

router.beforeEach((to, from, next) => {
    // check if lang has been set
    const langState = getLangState()

    // if the language hasn't already been set
    if (!langState) {
        // run the lang setter logic
        setLang(to, from, next)
    } else {
        // otherwise, just skip and proceed
        next()
    }
})

export default router
