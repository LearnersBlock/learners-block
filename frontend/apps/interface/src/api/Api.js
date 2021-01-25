import Vue from 'vue'
import store from '../store'
import axios from 'axios'
import Cookies from 'js-cookie'

export default () => {
    // Prepare axios config
    const config = {
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        }
    }

    // Set auth cookie identifier
    const authCookieName = 'lb__auth'

    // Attempt to get the auth token from the cookies
    const localAuthData = Cookies.get(authCookieName) ? JSON.parse(Cookies.get(authCookieName)) : null

    // If data was returned
    if (localAuthData) {
        // Get the access token
        const accessToken = localAuthData.token || ''

        // And add the header
        config.headers.Authorization = `Bearer ${accessToken}`
    }

    // Get the backend API url based on the current hostname
    // this is needed as the production environment hostname can be changed any time
    const backendUrl = process.env.VUE_APP_API_BASE || location.origin

    // Initiate the axios instance
    const Api = axios.create({
        baseURL: backendUrl + '/api/v1',
        ...config
    })

    // Add a custom interceptor
    Api.interceptors.response.use((response) => {
        // All good, just return the response (2xx)
        return response
    }, async (error) => {
        // Error to handle (i.e. 4xx)
        if (error.response && error.response.data) {
            // Check if we got a 401 error from the backend
            if (error.response.data.status === 401) {
                // If that's the case, assume the JWT token is either missing or invalid
                // force logout the user
                store.dispatch('auth/logout')

                // Get current path
                const currentPath = Vue.$router.history.current.path

                // Redirect to login
                Vue.$router.push(`/login?redirect=${currentPath}`)

                // Return the error
                return error.response
            }
        }

        // Continue
        return Promise.reject(error)
    })

    // Return the axios instance
    return Api
}
