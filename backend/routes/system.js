const SystemController = () => {
    // load dependencies
    const axios = require('axios').default
    const isValidHostname = require('is-valid-hostname')



    /**
     * /api/v1/system/info
     *
     * GET Endpoint to fetch system infos
     *
     * @since 1.0.0
     */

    const getSystemInfo = async (req, res) => {
        // query the wifi container status
        await axios.get(`${process.env.DEVICE_API_BASE}/system/info`)
            .then(function (response) {
                // handle success
                return res.json({
                    success: true,
                    data: {
                        ...response.data
                    }
                })
            })
            .catch(function (error) {
                // handle error
                if (error.response && error.response.data) {
                    // server responded with a status outside the 2xx but
                    // contains specific data to be passed to the frontend
                    return res.status(error.response.status).json({
                        success: false,
                        ...error.response.data
                    })
                } else {
                    // something else, most likely unknown, happened
                    return res.status(error.response.status).json({
                        success: false,
                        status: error.response.status,
                        message: error.response.statusText
                    })
                }
            })
    }



    /**
     * /api/v1/system/wifi/status
     *
     * GET Endpoint to fetch the device's wifi status (i.e. connected or disconnected)
     *
     * @since 1.0.0
     */

    const getWifiStatus = async (req, res) => {
        // query the wifi container status
        await axios.get(`${process.env.DEVICE_API_BASE}/wifi/connectionstatus`)
            .then(function (response) {
                // handle success
                return res.json({
                    success: true,
                    ...response.data
                })
            })
            .catch(function (error) {
                // handle error
                if (error.response && error.response.data) {
                    // server responded with a status outside the 2xx but
                    // contains specific data to be passed to the frontend
                    return res.status(error.response.status).json({
                        success: false,
                        ...error.response.data
                    })
                } else {
                    // something else, most likely unknown, happened
                    return res.status(error.response.status).json({
                        success: false,
                        status: error.response.status,
                        message: error.response.statusText
                    })
                }
            })
    }



    /**
     * /api/v1/system/wifi/reset
     *
     * POST Endpoint to reset the device's wifi connection
     *
     * @since 1.0.0
     */

    const resetWifiConnection = async (req, res) => {
        // query the wifi container status
        await axios.post(`${process.env.DEVICE_API_BASE}/wifi/forget`)
            .then(function (response) {
                // handle success
                return res.json({
                    success: true,
                    ...response.data
                })
            })
            .catch(function (error) {
                // handle error
                if (error.response && error.response.data && error.response.data.data) {
                    // server responded with a status outside the 2xx but
                    // contains specific data to be passed to the frontend
                    return res.status(error.response.status).json({
                        success: false,
                        ...error.response.data
                    })
                } else {
                    // something else, most likely unknown, happened
                    return res.status(error.response.status).json({
                        success: false,
                        status: error.response.status,
                        message: error.response.statusText
                    })
                }
            })
    }



    /**
     * /api/v1/system/hostname
     *
     * PATCH Endpoint to update the device's hostname
     *
     * @param req.body.hostname {String} The new hostname
     * @since 1.0.0
     */

    const updateHostname = async (req, res) => {
        // make sure we have a hostname
        if (!req.body.hostname) {
            return res.status(400).json({
                success: false,
                status: 400,
                error: 'Missing parameter(s): Hostname'
            })
        }

        // check the hostname is actually valid
        if (isValidHostname(req.body.hostname)) {
            // query the wifi container status
            await axios.patch(`${process.env.DEVICE_API_BASE}/hostconfig/${req.body.hostname}`)
                .then(function (response) {
                    // set ssid key
                    response.data.ssid = response.data.hostname

                    // handle success
                    return res.json({
                        success: true,
                        ...response.data
                    })
                })
                .catch(function (error) {
                    // handle error
                    if (error.response && error.response.data) {
                        // server responded with a status outside the 2xx but
                        // contains specific data to be passed to the frontend
                        return res.status(error.response.status).json({
                            success: false,
                            ...error.response.data
                        })
                    } else {
                        // something else, most likely unknown, happened
                        return res.status(error.response.status).json({
                            success: false,
                            status: error.response.status,
                            message: error.response.statusText
                        })
                    }
                })
        } else {
            return res.status(400).json({
                success: false,
                status: 400,
                error: 'Invalid parameter(s): Hostname'
            })
        }
    }





    /**
     * /api/v1/system/database/reset
     *
     * POST Endpoint to reset the backend database
     *
     * @since 1.0.0
     */

    const resetDatabase = async (req, res) => {
        // access the individual controllers
        const AuthController = require('./auth')()
        const SettingsController = require('./settings')()

        // trigger database rebuild
        const AuthDatabaseReset = await AuthController.reset()
        const SettingsDatabaseReset = await SettingsController.reset()

        // check if both actions were successfull
        if (AuthDatabaseReset && SettingsDatabaseReset) {
            // return success
            return res.status(200).json({
                success: true,
                status: 200,
                error: 'Database reset was completed.'
            })
        } else {
            return res.status(500).json({
                success: false,
                status: 500,
                error: 'An error occurred and the database could not be reset.'
            })
        }
    }



    /**
     * return functions
     *
     * @since 1.0.0
     */

    return {
        getSystemInfo,
        getWifiStatus,
        resetWifiConnection,
        updateHostname,
        resetDatabase
    }
}

module.exports = SystemController
