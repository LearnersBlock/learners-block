export default {
    methods: {
        getFileviewerLink: function (admin) {
            // get fileviewer settings and current locale
            const link = this.$store.state.settings.settings.components.fileviewer.path
            const lang = this.$i18n.locale

            // prepare admin params
            let adminParams = {}

            // set public params
            const publicParams = {
                lang: lang
            }

            // if admin access was requested
            if (admin) {
                // check auth
                if (this.$store.getters['auth/isAuthenticated']) {
                    // set admin params
                    adminParams = {
                        mode: 'admin'
                    }
                }
            }

            // merge params
            const params = { ...publicParams, ...adminParams }

            // create query string
            const queryString = this.createQueryParams(params)

            // return built link
            return `${link}/?${queryString}`
        }
    }
}
