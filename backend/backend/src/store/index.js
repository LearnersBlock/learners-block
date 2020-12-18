import Vue from 'vue'
import Vuex from 'vuex'

import app from './modules/app'
import auth from './modules/auth'
import lang from './modules/lang'
import settings from './modules/settings'

import createLogger from 'vuex/dist/logger'

Vue.use(Vuex)

export default new Vuex.Store({
    plugins: [createLogger()],
    modules: {
        app,
        auth,
        lang,
        settings
    }
})
