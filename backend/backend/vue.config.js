process.env.VUE_APP_VERSION = require('./package.json').version

module.exports = {
    chainWebpack: (config) => {
        const svgRule = config.module.rule('svg')

        svgRule.uses.clear()

        svgRule
            .use('babel-loader')
            .loader('babel-loader')
            .end()
            .use('vue-svg-loader')
            .loader('vue-svg-loader')
    },

    css: {
        loaderOptions: {
            sass: {
                prependData: `
                    @import "@/scss/_core/_vars.scss";
                    @import "@/scss/_core/_mixins.scss";
                `
            }
        }
    },

    pluginOptions: {
        i18n: {
            locale: 'en',
            fallbackLocale: 'en',
            localeDir: 'lang',
            enableInSFC: true
        }
    }
}
