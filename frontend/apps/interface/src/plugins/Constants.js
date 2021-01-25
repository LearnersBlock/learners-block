/**
 * Constants
 *
 * Vue.js plugin to provide various constant variables to the app
 *
 * @returns {Object} Object of constant variables used in the app
 */
const Constants = {
    install (Vue, options) {
        // Get the container/frontend url
        const frontendUrl = process.env.VUE_APP_API_BASE || location.protocol + '//' + location.hostname

        // Remove the port (i.e. :8081) from the URL
        const portRegex = /:\d+$/
        const frontendHost = frontendUrl.replace(portRegex, '')

        // Create global constants
        Vue.prototype.$constants = {
            WEBSITE: '/website',
            FILEMANAGER: '/files',
            WIFICONNECT: `${frontendHost}:8080`
        }
    }
}

export default Constants
