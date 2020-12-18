<template>
    <div>
        <div v-if="!this.$store.state.auth.required" class="el-section__group">
            <el-alert
                :title="$t('settings-screen.auth.disabled.title')"
                :description="$t('settings-screen.auth.disabled.description')">
            </el-alert>
        </div>

        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.auth.account.title') }}</h5>
            </div>

            <div class="el-section__content" v-loading="this.loading">
                <el-form ref="authSettings" :model="authSettings"
                :rules="authSettingsRules" label-width="">
                    <el-form-item label="" align="left" prop="username">
                        <el-input v-model="authSettings.username" placeholder="Username">
                            <i slot="prefix">
                                <el-icon name="heroicons-user" type="light" classes="el-input__icon"></el-icon>
                            </i>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="" align="left" prop="password">
                        <el-input
                            v-model="authSettings.password"
                            placeholder="Password" required>
                            <i slot="prefix">
                                <el-icon name="heroicons-key" type="light" classes="el-input__icon"></el-icon>
                            </i>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="">
                        <password
                            v-model="authSettings.password"
                            :strength-meter-only="true"
                            @score="updateSubmitState">
                        </password>
                    </el-form-item>

                    <el-button
                        @click="submitAccountForm()"
                        type=" el-button--block"
                        :class="!submitDisabled ? 'el-button--success' : ''"
                        :disabled="submitDisabled"
                        plain>
                        {{ $t('general.save') }}
                    </el-button>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
import Api from '@/api/Api'
import store from '@/store'

import Password from 'vue-password-strength-meter'

import ElAlert from '@/components/Alerts/Alert'
import ElIcon from '@/components/Icons/Icon'

export default {
    name: 'SettingsUsers',
    components: {
        ElIcon,
        ElAlert,
        Password
    },
    mixins: [],
    data () {
        return {
            error: null,
            loading: false,
            submitDisabled: true,
            authSettings: {
                username: this.$store.state.auth.username || null,
                password: null
            },
            authSettingsRules: {}
        }
    },
    computed: {},
    methods: {
        updateSubmitState: function (score) {
            if (score >= 3) {
                this.submitDisabled = false
            } else {
                this.submitDisabled = true
            }
        },

        submitAccountForm: function () {
            // check if the auth requirement is set
            const accountExists = store.getters['auth/isAuthRequired']

            // if the account exists
            if (accountExists) {
                // run it as an update
                this.updateUserAccount()
            } else {
                // or, create the account
                this.createUserAccount()
            }
        },

        createUserAccount: function () {
            // loading state
            this.loading = true

            // trigger API request
            Api()
                .post('/users', {
                    ...this.authSettings
                })
                .then((response) => {
                    // reset request was successful
                    // force logout
                    this.$store.dispatch('auth/logout')
                        .then((result) => {
                            setTimeout(() => {
                                this.$router.go('/login')
                            }, 300)
                        })
                })
                .catch((err) => {
                    // reset request returned an error
                    console.error(err) // eslint-disable-line

                    // loading state
                    this.loading = false
                })
        },

        updateUserAccount: function () {
            // loading state
            this.loading = true

            // trigger API request
            Api()
                .patch('/users', {
                    id: this.$store.state.auth.username,
                    ...this.authSettings
                })
                .then((response) => {
                    // reset request was successful
                    // force logout
                    this.$store.dispatch('auth/logout')
                        .then((result) => {
                            setTimeout(() => {
                                this.$router.go('/login')
                            }, 300)
                        })
                })
                .catch((err) => {
                    // reset request returned an error
                    console.error(err) // eslint-disable-line

                    // loading state
                    this.loading = false
                })
        }
    },
    beforeRouteEnter: async function (to, from, next) {
        try {
            await Promise.all([
                store.dispatch('settings/fetchSettings')
            ]).then(() => {
                next()
            })
        } catch (error) {
            next('/500')
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_forms/form.base';
@import '@/scss/_components/_forms/_inputs/input.base';
@import '@/scss/_plugins/plugin.passwordmeter';
</style>
