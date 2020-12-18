export default {
    methods: {
        updateSetting: function (group, key, val) {
            // prepare params
            const params = {
                group: group,
                key: key,
                value: val
            }

            // dispatch API request via store
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
