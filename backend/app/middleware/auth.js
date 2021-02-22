const AuthMiddleware = () => {
    // load dependencies
    const low = require('lowdb')
    const FileSync = require('lowdb/adapters/FileSync')
    const jwt = require('jsonwebtoken')


    /**
     * verifyJWT()
     *
     * Middleware to verify the JWT token
     *
     * @since 1.0.0
     */

    const verifyJWT = (req, res, next) => {
        // init filesync adapter and database
        const adapter = new FileSync('db/auth.json')
        const db = low(adapter)

        // fetch db state
        db.read()

        // check within the DB wether auth is enabled
        const authEnabled = db.get('settings.enabled').value()

        // if auth is enabled
        if (authEnabled) {
            // get the auth header
            const authHeader = req.headers.authorization

            // check that an auth header was passed
            if (authHeader) {
                // if so, get the token from the Bearer string
                const token = authHeader.split(' ')[1]

                // verify the token
                jwt.verify(token, process.env.APP_JWT_SECRET, (err, user) => {
                    if (err) {
                        return res.status(401).json({
                            success: false,
                            status: 401,
                            data: 'Token missing or invalid. Please re-authenticate and try again.'
                        })
                    }

                    req.user = user
                    next()
                })
            } else {
                return res.status(401).json({
                    success: false,
                    status: 401,
                    data: 'Token missing or invalid. Please re-authenticate and try again.'
                })
            }
        } else {
            // otherwise, if auth is disabled just skip all this
            next()
        }
    }

    return {
        verifyJWT
    }
}

module.exports = AuthMiddleware
