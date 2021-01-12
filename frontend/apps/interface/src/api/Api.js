import Vue from 'vue'
import store from '../store'
import axios from 'axios'
import Cookies from 'js-cookie'

export default () => {
    // prepare axios config
    const config = {
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        }
    }

    // set auth cookie identifier
    const authCookieName = 'lb__auth'

    // attempt to get the auth token from the cookies
    const localAuthData = Cookies.get(authCookieName) ? JSON.parse(Cookies.get(authCookieName)) : null

    // if data was returned
    if (localAuthData) {
        // get the access token
        const accessToken = localAuthData.token || ''

        // and add the header
        config.headers.Authorization = `Bearer ${accessToken}`
    }

    // get the backend API url based on the current hostname
    // this is needed as the production environment hostname can be changed any time
    const backendUrl = process.env.VUE_APP_API_BASE || location.origin

    // initiate the axios instance
    const Api = axios.create({
        baseURL: backendUrl + '/api/v1',
        ...config
    })

    // add a custom interceptor
    Api.interceptors.response.use((response) => {
        // all good, just return the response (2xx)
        return response
    }, async (error) => {
        // error to handle (i.e. 4xx)
        if (error.response && error.response.data) {
            // check if we got a 401 error from the backend
            if (error.response.data.status === 401) {
                // if that's the case, assume the JWT token is either missing or invalid
                // force logout the user
                store.dispatch('auth/logout')

                // get current path
                const currentPath = Vue.$router.history.current.path

                // redirect to login
                Vue.$router.push(`/login?redirect=${currentPath}`)

                return error.response
            }
        }

        // continue
        return Promise.reject(error)
    })

    // return the axios instance
    return Api
}
