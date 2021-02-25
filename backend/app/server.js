/**
 * Dependencies
 *
 * @since 1.0.0
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

// server
const express = require('express')
const helmet = require('helmet')

const port = process.env.PORT || 3001
const app = express()

// dotenv
require('dotenv').config()

// plugins & Dependencies
const bodyParser = require('body-parser')

// configure
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.use(helmet())

// routing conf
const apiBase = '/api/v1'



/**
 * Headers
 *
 * @since 1.0.0
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

app.use(function (req, res, next) {
    // Determine the frontend URL for the CORS headers
    // Note: This is needed as in production, the hostname can be changed freely.
    // Therefore, make sure to only provide an APP_URL env var in development
    // when running a Vue.js dev server on localhost:3000
    const frontendUrl = process.env.APP_URL || req.protocol + '://' + req.get('host')
    
    // Set headers
    res.setHeader('Access-Control-Allow-Origin', frontendUrl)
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PATCH,OPTIONS')
    res.setHeader('Access-Control-Allow-Credentials', true)
    res.setHeader('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')

    // Pass to next layer of middleware
    next()
})



/**
 * Static Files
 *
 * @since 1.0.0
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

app.use('/files', express.static('static'))



/**
 * Routes
 *
 * @since 1.0.0
 * –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

const AuthMiddleware = require('./middleware/auth')()

const AuthController = require('./routes/auth')()
const SettingsController = require('./routes/settings')()
const SystemController = require('./routes/system')()

// auth
app.get(`${apiBase}/auth/check`, AuthController.check)
app.post(`${apiBase}/auth/login`, AuthController.login)
app.post(`${apiBase}/auth/validate`, AuthController.validateToken)

// users
app.post(`${apiBase}/users`, AuthController.createUser)
app.patch(`${apiBase}/users`, AuthMiddleware.verifyJWT, AuthController.updateUser)

// settings
app.get(`${apiBase}/settings`, SettingsController.getAll)
app.patch(`${apiBase}/settings`, AuthMiddleware.verifyJWT, SettingsController.updateSetting)

// system
app.get(`${apiBase}/system/info`, SystemController.getSystemInfo)
app.get(`${apiBase}/system/wifi/status`, AuthMiddleware.verifyJWT, SystemController.getWifiStatus)
app.post(`${apiBase}/system/wifi/reset`, AuthMiddleware.verifyJWT, SystemController.resetWifiConnection)
app.post(`${apiBase}/system/database/reset`, AuthMiddleware.verifyJWT, SystemController.resetDatabase)
app.patch(`${apiBase}/system/hostname`, AuthMiddleware.verifyJWT, SystemController.updateHostname)

// default
app.get('/', function (req, res) {
    // redirect to application
    res.redirect(process.env.APP_URL)
})



/**
 *  Server Application
 *
 *  @since 1.0.0
 *  ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– */

app.listen(port, function(){
    console.log(`REST API running on localhost:${port}`)
})

module.exports = app