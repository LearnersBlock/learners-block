export default {
    methods: {
        /**
         * Create URL friendly query parameters from an object
         *
         * @param   {String} group The settings group to update
         * @param   {String} key   The key value to target inside the group
         * @param   {String} val   The value to save/update
         * @returns void
         */
        updateSetting: function (group, key, val) {
            // Prepare params
            const params = {
                group: group,
                key: key,
                value: val
            }

            // Dispatch API request via store
            this.$store.dispatch('settings/update', params)
                .then((result) => {})
                .catch((error) => {
                    // @TODO add error handling, i.e. show user settings could
                    // not be updated
                    console.warn(error) // eslint-disable-line
                })
        }
    }
}
