<template>
    <div class="el-auth el-auth--logout">
        <div class="el-auth__inner">
            <div class="el-auth__title">
                <p>{{ this.title }}</p>
            </div>
            <div class="el-auth__loader" v-loading="this.isAuthLoading"></div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: 'AuthLogout',
    data () {
        return {}
    },
    props: {
        title: String
    },
    computed: {
        ...mapGetters('auth', [
            'isAuthLoading'
        ])
    },
    methods: {},
    mounted: function () {
        /**
         * Mounted: Logout
         *
         * @returns void
         */
        this.$store.dispatch('auth/logout')
            .then((result) => {
                // check if we have a redirect param
                if (this.$router.history.current.query.redirect) {
                    // if so, push to that page
                    this.$router.push(this.$router.history.current.query.redirect)
                } else {
                    // otherwise just go back to where the logout was initiated
                    this.$router.go(-1)
                }
            })
    }
}
</script>

<style lang="scss">
@import 'Auth';
</style>
