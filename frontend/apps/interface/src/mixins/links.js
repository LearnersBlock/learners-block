export default {
    methods: {
        /**
         * Create URL friendly query parameters from an object
         *
         * @param {Object} params The params to encore
         */
        createQueryParams: function (params) {
            return Object.keys(params)
                .map(k => `${k}=${encodeURI(params[k])}`)
                .join('&')
        },

        /**
         * Generate URLs for external components based on specific parameters
         *
         * @param {String}      link    The link to use as base
         * @param {String|Null} lang    The key to use as lang parameter, or null to disable
         * @param {Boolean}     admin   Whether or not request admin mode access
         */
        getExternalLink: function (link, lang, admin) {
            // Ensure that a link has been provided
            if (!link) {
                return false
            }

            // Prepare admin params
            const adminParams = {}

            // Prepare public params
            const publicParams = {}

            // Check if the lang key was passed
            if (lang) {
                // If so, push is to the public params obj, using the lang as key
                publicParams[lang] = this.$i18n.locale
            }

            // Check if admin access was requested
            if (admin) {
                // If so, check if user is authenticated before proceeding
                if (this.$store.getters['auth/isAuthenticated']) {
                    // If authenticated, add the admin param
                    adminParams.mode = 'admin'
                }
            }

            // Merge public & admin params params
            const params = { ...publicParams, ...adminParams }

            // Create the query string
            const queryString = this.createQueryParams(params)

            // Return built link
            return `${link}/?${queryString}`
        }
    }
}
