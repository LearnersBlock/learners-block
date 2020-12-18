/**
 * Dependencies
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

// server
const express = require('express')

const port = process.env.PORT || 3002
const app = express()


// plugins & Dependencies
const bodyParser = require('body-parser')

// configure
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

// routing conf
const apiBase = '/api/v1'


/**
 * Routes
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

/**
 * GET /api/v1/wifi/status
 */

app.get(`${apiBase}/wificonnectionstatus`, (req, res) => {
    const testcase = 1
    const timeout = Math.floor(Math.random() * 2000)

    if (testcase === 1) {
        setTimeout(function () {
            return res.status(200).json({
                status: 200,
                connection: 'connected',
                testdata: {
                    case: testcase,
                    timeout: timeout,
                    message: 'Device is connected to a WiFi network.'
                }
            })
        }, timeout)
    }

    if (testcase === 2) {
        return res.status(206).json({
            status: 206,
            connection: 'disconnected',
            testdata: {
                case: testcase,
                timeout: timeout,
                message: 'Device is not connected to a WiFi network.'
            }
        })
    }

    if (testcase === 3) {
        return res.status(500).json({
            status: 500,
            connection: 'error',
            testdata: {
                case: testcase,
                timeout: timeout,
                message: 'An unknown error occured. Well damn it.'
            }
        })
    }
})

/**
 * POST /api/v1/wifi/reset
 */

app.post(`${apiBase}/wififorget`, (req, res) => {
    const testcase = 1
    const timeout = Math.floor(Math.random() * 5000)

    if (testcase === 1) {
        setTimeout(function () {
            return res.status(202).json({
                status: 202,
                message: 'Connection was reset.',
                testdata: {
                    case: testcase,
                    timeout: timeout
                }
            })
        }, timeout)
    }

    if (testcase === 2) {
        return res.status(409).json({
            status: 409,
            message: 'Device is already disconnected, cannot be reset.',
            testdata: {
                case: testcase,
                timeout: timeout
            }
        })
    }

    if (testcase === 3) {
        return res.status(500).json({
            status: 500,
            message: 'Device is connected but could not reset the connection.',
            testdata: {
                case: testcase,
                timeout: timeout
            }
        })
    }
})

/**
 * PATCH /api/v1/hostconfig/:hostname
 */

app.patch(`${apiBase}/hostconfig/:hostname`, (req, res) => {
    const testcase = 3
    const timeout = Math.floor(Math.random() * 5000)

    if (testcase === 1) {
        setTimeout(function () {
            return res.status(200).json({
                status: 200,
                hostname: req.params.hostname,
                message: `Hostname was updated to ${req.params.hostname}`,
                testdata: {
                    case: testcase,
                    timeout: timeout
                }
            })
        }, timeout)
    }

    if (testcase === 2) {
        setTimeout(function () {
            return res.status(400).json({
                status: 400,
                hostname: null,
                message: 'One or more parameters are missing.',
                testdata: {
                    case: testcase,
                    timeout: timeout
                }
            })
        }, timeout)
    }

    if (testcase === 3) {
        setTimeout(function () {
            return res.status(500).json({
                status: 500,
                hostname: req.params.hostname,
                message: `Hostname could not be updated to ${req.params.hostname}`,
                testdata: {
                    case: testcase,
                    timeout: timeout
                }
            })
        }, timeout)
    }
})

/**
 * GET /api/v1/versions
 */

app.get(`${apiBase}/versions`, (req, res) => {
    return res.status(200).json({
        lb: '0.0.1',
        frontend: '0.0.1',
        backend: '0.0.1',
        controller: '0.0.1',
        ifm: '0.0.1',
        wificonnect_ui: '0.0.1'
    })
})


/**
 * Server Application
 * ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

app.listen(port, function () {
    console.log(`Device test API running on localhost:${port}`)
})

module.exports = app