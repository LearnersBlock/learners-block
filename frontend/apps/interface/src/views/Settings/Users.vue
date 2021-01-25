<template>
    <div>
        <SettingsGroupContainer :loading="this.loading">
            <template v-slot:title>
                <h5>{{ accountGroupTitle }}</h5>
            </template>

            <template v-slot:content>
                <el-form
                    ref="authSettings"
                    :model="authSettings"
                    :rules="authSettingsRules"
                    label-width="">
                    <el-form-item label="" align="left" prop="username">
                        <el-input v-model="authSettings.username" placeholder="Username">
                            <i slot="prefix">
                                <Icon name="heroicons-user" type="light" classes="el-input__icon"></Icon>
                            </i>
                        </el-input>
                    </el-form-item>

                    <el-form-item label="" align="left" prop="password">
                        <el-input
                            v-model="authSettings.password"
                            placeholder="Password" required>
                            <i slot="prefix">
                                <Icon name="heroicons-key" type="light" classes="el-input__icon"></Icon>
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

                    <Button
                        :type="!submitDisabled ? 'success' : ''"
                        size="block"
                        :plain="true"
                        :disabled="submitDisabled"
                        @clicked="submitAccountForm()">
                        {{ $t('general.save') }}
                    </Button>
                </el-form>
            </template>
        </SettingsGroupContainer>
    </div>
</template>

<script>
import Api from '@/api/Api'
import store from '@/store'

import Password from 'vue-password-strength-meter'

import SettingsGroupContainer from '@/components/Containers/SettingsGroup'
import Button from '@/components/Button/Button'
import Icon from '@/components/Icons/Icon'

export default {
    name: 'SettingsUsers',
    components: {
        SettingsGroupContainer,
        Icon,
        Button,
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
    computed: {
        /**
         * Computes the account title based on current auth status
         */
        accountGroupTitle: function () {
            // Check if we have a username stored in the settings
            if (this.authSettings.username) {
                // If so, assume we're editing the account
                return this.$t('settings-screen.auth.account.existing.title')
            }

            // Otherwise, assume this is a new account
            return this.$t('settings-screen.auth.account.new.title')
        }
    },
    methods: {
        /**
         * Set submit button disabled state based on password strength
         *
         * @param   {Integer} score The password strength score
         * @returns void
         */
        updateSubmitState: function (score) {
            // If password score is above 3/5
            if (score >= 3) {
                // Enable button
                this.submitDisabled = false
            } else {
                // Otherwise, disable it
                this.submitDisabled = true
            }
        },

        /**
         * Submit the account form
         *
         * @returns void
         */
        submitAccountForm: function () {
            // Check if the auth requirement is set
            const accountExists = store.getters['auth/isAuthRequired']

            // If the account exists
            if (accountExists) {
                // Run it as an update
                this.updateUserAccount()
            } else {
                // Otherwise, create the account
                this.createUserAccount()
            }
        },

        /**
         * Create user account
         *
         * @returns void
         */
        createUserAccount: function () {
            // Set the loading state
            this.loading = true

            // Trigger the API request
            Api()
                .post('/users', {
                    ...this.authSettings
                })
                .then((response) => {
                    // Account creation request was successful
                    // Force logout
                    this.$store.dispatch('auth/logout')
                        .then((result) => {
                            setTimeout(() => {
                                // Redirect to login
                                this.$router.go('/login')
                            }, 300)
                        })
                })
                .catch((err) => {
                    // Account creation request returned an error
                    // @TODO improve error handling
                    console.error(err) // eslint-disable-line

                    // Set loading state
                    this.loading = false
                })
        },

        /**
         * Update user account
         *
         * @returns void
         */
        updateUserAccount: function () {
            // Set loading state
            this.loading = true

            // Trigger the API request
            Api()
                .patch('/users', {
                    id: this.$store.state.auth.username,
                    ...this.authSettings
                })
                .then((response) => {
                    // Update request was successful
                    // Force logout
                    this.$store.dispatch('auth/logout')
                        .then((result) => {
                            setTimeout(() => {
                                // Redirect to login
                                this.$router.go('/login')
                            }, 300)
                        })
                })
                .catch((err) => {
                    // Update request returned an error
                    // @TODO improve error handling
                    console.error(err) // eslint-disable-line

                    // Set loading state
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
