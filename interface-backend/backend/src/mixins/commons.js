export default {
    methods: {
        createQueryParams: function (params) {
            return Object.keys(params)
                .map(k => `${k}=${encodeURI(params[k])}`)
                .join('&')
        }
    }
}
