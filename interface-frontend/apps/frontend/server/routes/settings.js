const SettingsController = () => {
    // load dependencies
    const path = require('path')
    const fs = require('fs')
    const low = require('lowdb')
    const FileSync = require('lowdb/adapters/FileSync')

    // settings
    const DatabasePath = path.resolve('db/settings.json')
    const DatabaseSeedPath = path.resolve('seeds/seeds.settings.js')

    // init filesync adapter and database
    const adapter = new FileSync(DatabasePath)
    const db = low(adapter)

    // set default db table structure
    const defaults = require(DatabaseSeedPath)

    // write the defaults to the db file
    db.defaults({ ...defaults })
        .write()


    /**
     * GET /api/v1/settings
     *
     * @since 1.0.0
     */

    const getAll = (req, res) => {
        // get all settings
        const result = db.get('settings', false)
            .value()

        // check if we have data to return
        if (result) {
            // if so, return the results
            return res.json({
                success: true,
                status: 200,
                data: result
            })
        } else {
            // otherwise, server 404 error
            return res.status(404).json({
                success: false,
                status: 404,
                data: 'No data found'
            })
        }
    }

    /**
     * PATCH /api/v1/settings
     *
     * @since 1.0.0
     */

    const updateSetting = (req, res) => {
        // make sure we have both key and value
        if (!req.body.group || !req.body.key || req.body.value === 'undefined') {
            // otherwise, server 400 error
            return res.status(400).json({
                success: false,
                status: 400,
                data: 'Bad request'
            })
        }

        // make sure the requested setting to update exists
        if (!db.has(`settings.${req.body.group}.${req.body.key}`).value()) {
            // otherwise, return 404 error
            return res.status(400).json({
                success: false,
                status: 404,
                data: 'Setting not found'
            })
        }

        // convert string to booleans where applicable
        if (req.body.value === 'true') {
            req.body.value = true
        } else if (req.body.value === 'false') {
            req.body.value = false
        }

        // update the requested setting
        const result = db.get(`settings.${req.body.group}`)
            .assign({ [req.body.key]: req.body.value })
            .write()

        // check if we have data to return
        if (result) {
            // if so, return the results
            return res.json({
                success: true,
                status: 200,
                data: result
            })
        } else {
            // otherwise, server 404 error
            return res.status(500).json({
                success: false,
                status: 500,
                data: 'Internal server error'
            })
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
        getAll,
        updateSetting,
        reset
    }
}

module.exports = SettingsController
