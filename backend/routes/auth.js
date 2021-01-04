const AuthController = () => {
    // load dependencies
    const path = require('path')
    const fs = require('fs')
    const crypto = require('crypto')
    const low = require('lowdb')
    const FileSync = require('lowdb/adapters/FileSync')
    const jwt = require('jsonwebtoken')

    // settings
    const DatabasePath = path.resolve('db/auth.json')
    const DatabaseSeedPath = path.resolve('seeds/seeds.auth.js')

    // init filesync adapter and database
    const adapter = new FileSync(DatabasePath)
    const db = low(adapter)

    // get db table seeds
    const defaults = require(DatabaseSeedPath)

    // write the defaults to the db file
    db.defaults({ ...defaults })
        .write()


    /**
     * getUsers()
     *
     * Helper function to retrieve the full list of users
     *
     * @since 1.0.0
     */

    const getUsers = () => {
        // fetch db state
        db.read()

        // get users from db
        const users = db.get('users').value()

        // return results
        return users
    }

    /**
     * generateEncodedPassword()
     *
     * Helper function to encode a user password
     *
     * @param password {String} The password to encode
     * @since 1.0.0
     */

    const generateEncodedPassword = (password) => {
        // get the encoded password
        const salt = crypto.randomBytes(16).toString('base64')
        const hash = crypto.createHmac('sha512', salt).update(password).digest('base64')

        // return the salt and hash combination
        return `${salt}$${hash}`
    }

    /**
     * validateUserCredentials()
     *
     * Helper function to validate user credentials
     *
     * @param username {String} The username to validate
     * @param password {String} The password to validate against
     * @since 1.0.0
     */

    const validateUserCredentials = (username, password) => {
        // fetch db state
        db.read()

        // get the users and find our username
        const user = db.get('users').find({ username: username }).value()

        // check that we have a result
        if (!user) {
            // if that's not the case, abort
            return false
        } else {
            // otherwise, proceed and validate the password
            // separate salt and hash from db entry
            const passwordFields = user.password.split('$')

            // encode password for verification
            const salt = passwordFields[0]
            const hash = crypto.createHmac('sha512', salt).update(password).digest('base64')

            // compare if passwords match
            if (hash === passwordFields[1]) {
                // if so, confirm by returning the user entry
                return {
                    ...user
                }
            } else {
                // otherwise, abort
                return false
            }
        }
    }

    /**
     * updateUserRecord()
     *
     * Helper function to update a specific user record
     *
     * @param username {String} The username to update
     * @param newUsername {String} The new username to insert
     * @param newPassword {String} The new password to insert
     * @since 1.0.0
     */

    const updateUserRecord = (username, newUsername, newPassword) => {
        // prepare update
        let updateData = {}

        // add a new username if it is to be updated
        if (newUsername) {
            updateData.username = newUsername
        }

        // add a new password if is to be updated
        if (newPassword) {
            updateData.password = generateEncodedPassword(newPassword)
        }

        // run the db update
        const user = db.get('users')
            .find({ username: username })
            .assign(updateData)
            .write()

        // return results
        return updateData
    }


    /**
     * enableAuthRequirement()
     *
     * Helper function to update the auth requirement for the application
     *
     * @param value {Boolean} The value to set to the db
     * @since 1.0.0
     */

    const enableAuthRequirement = function (value) {
        // update db value
        const updateAuthReq = db.set('settings.enabled', value).write()

        // return results
        return updateAuthReq
    }



    /**
     * GET /api/v1/auth/check
     *
     * Endpoint to check if auth is currently required on the system
     *
     * @since 1.0.0
     */

    const check = (req, res) => {
        // fetch db state
        db.read()

        // check within the DB wether auth is enabled
        const authEnabled = db.get('settings.enabled').value()

        // if auth is enabled or disabled
        if (authEnabled === true || authEnabled === false) {
            // return a response containing the information
            return res.status(200).json({
                success: true,
                status: 200,
                data: {
                    enabled: authEnabled
                }
            })
        } else {
            // otherwise, 500 server error
            return res.status(500).json({
                success: false,
                status: 500,
                data: 'Auth status could not be fetched'
            })
        }
    }



    /**
     * POST /api/v1/users
     *
     * Endpoint to create a new user
     *
     * @param req.body.username {String} The username
     * @param req.body.password {String} The password
     * @since 1.0.0
     */

    const createUser = (req, res) => {
        // check that we have all needed params to create an account
        if (!req.body.username || !req.body.password) {
            // otherwise, server 400 error
            return res.status(400).json({
                success: false,
                status: 400,
                data: 'Missing required parameter(s).'
            })
        }

        // now check that we don't have any other users in the DB as we currently
        // only allow for one unique user to exist
        const users = getUsers()

        // if the response is not empty
        if (users.length) {
            // return an error
            return res.status(403).json({
                success: false,
                status: 403,
                data: 'You do not have the permissions required to create a new user.'
            })
        }

        // otherwise, proceed with the user creation
        req.body.password = generateEncodedPassword(req.body.password)

        // set permissions level
        req.body.permissions = 'admin'

        // prepare user data
        const userData = {
            username: req.body.username,
            password: req.body.password,
            permissions: req.body.permissions
        }

        // and finally, insert user into the db
        const userEntry = db.get('users').push(userData).write()

        // check the status
        if (userEntry) {
            // if successfull, force enable authentication
            enableAuthRequirement(true)

            // if successful, return 200
            return res.status(200).json({
                success: true,
                status: 200
            })
        } else {
            // otherwise, return 500
            return res.status(500).json({
                success: false,
                status: 500,
                data: 'A new user could not be created.'
            })
        }
    }



    /**
     * PATCH /api/v1/users
     *
     * Endpoint to update an existing user
     *
     * @param req.body.id {String} The current username
     * @param req.body.username {String} The new username
     * @param req.body.password {String} The new password
     * @since 1.0.0
     */

    const updateUser = (req, res) => {
        // check that we have all needed params to create an account
        if (!req.body.id || !req.body.username || !req.body.password) {
            // otherwise, server 400 error
            return res.status(400).json({
                success: false,
                status: 400,
                data: 'Missing required parameter(s).'
            })
        }

        // find the user and validate the account existence
        // fetch db state
        db.read()

        // get the users and find our username
        const user = db.get('users').find({ username: req.body.id }).value()

        // check if we found a user by that username
        if (!user) {
            // if that's not the case, return an error
            return res.status(403).json({
                success: false,
                status: 403,
                data: 'Username or password incorrect.'
            })
        } else {
            // update the DB entry
            const updateUserEntry = updateUserRecord(req.body.id, req.body.username, req.body.password)

            // return the results
            return res.status(200).json({
                success: true,
                status: 200,
                data: updateUserEntry
            })
        }
    }



    /**
     * POST /api/v1/auth/login
     *
     * Endpoint to authenticate a user
     *
     * @param req.body.username {String} The username
     * @param req.body.password {String} The password
     * @since 1.0.0
     */

    const login = (req, res) => {
        // check that username and password have been passed
        if (!req.body.username || !req.body.password) {
            // otherwise, server 400 error
            return res.status(400).json({
                success: false,
                status: 400,
                data: 'Missing credentials'
            })
        } else {
            // find the user and validate the credentials
            const user = validateUserCredentials(req.body.username, req.body.password)

            // check if we found a user by that username
            if (!user) {
                // if that's not the case, return an error
                return res.status(403).json({
                    success: false,
                    status: 403,
                    data: 'Username or password incorrect.'
                })
            } else {
                // get the access token
                const accessToken = jwt.sign({ username: user.username, role: user.role }, process.env.APP_JWT_SECRET, { expiresIn: '24h' })

                // return result
                return res.json({
                    success: true,
                    status: 200,
                    data: {
                        username: user.username,
                        permissions: user.permissions,
                        token: accessToken
                    }
                })
            }
        }
    }

    /**
     * reset
     *
     * @since 1.0.0
     */

    const reset = (req, res) => {
        // delete the DB file
        fs.unlink(DatabasePath, (err) => {
            // check if an error occured
            if (err) {
                // add logging
                console.warn(err)
                return false
            }

            // file was deleted
            // force update the db memory state
            db.read()

            // force reload the db seed
            const databaseSeeds = require(DatabaseSeedPath)

            // recreate from seeds
            db.defaults({ ...databaseSeeds }).write()
        })

        // return true for success
        return true
    }

    return {
        check,
        login,
        createUser,
        updateUser,
        reset
    }
}

module.exports = AuthController
