<template>
    <div class="el-auth">
        <div class="el-auth__inner" v-loading="this.isAuthLoading">
            <div class="el-auth__title">
                <h1>{{ this.title }}</h1>

                <p>{{ this.description }}</p>
            </div>

            <transition name="fade">
                <div v-show="authError.status" class="el-auth__error">
                    <Alert
                        type="error"
                        icon="heroicons-exclamation"
                        :title="this.authError.title"
                        :description="this.authError.message">
                    </Alert>
                </div>
            </transition>

            <div class="el-auth__form">
                <el-form
                    :model="authForm"
                    :rules="authFormRules"
                    ref="authForm">
                    <el-form-item prop="username">
                        <el-input
                            type="text"
                            v-model="authForm.username"
                            :placeholder="$t('auth-screen.login.username')">
                            <i slot="prefix">
                                <Icon name="heroicons-user" type="light" classes="el-input__icon" />
                            </i>
                        </el-input>
                    </el-form-item>

                    <el-form-item prop="password">
                        <el-input
                            type="password"
                            v-model="authForm.password"
                            :placeholder="$t('auth-screen.login.password')">
                            <i slot="prefix">
                                <Icon name="heroicons-key" type="light" classes="el-input__icon" />
                            </i>
                        </el-input>
                    </el-form-item>

                    <Button
                        type=""
                        size="block"
                        @clicked="submitForm('authForm')">
                        {{ $t('auth-screen.login.submit') }}
                    </Button>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Alert from '@/components/Alerts/Alert'
import Button from '@/components/Button/Button'
import Icon from '@/components/Icons/Icon'

export default {
    name: 'AuthLogin',
    components: {
        Alert,
        Button,
        Icon
    },
    data () {
        return {
            authError: {
                status: '',
                title: '',
                message: ''
            },

            authForm: {
                username: '',
                password: ''
            },

            authFormRules: {
                username: [
                    {
                        required: true,
                        message: '',
                        trigger: 'blur'
                    }
                ],
                password: [
                    {
                        required: true,
                        message: '',
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    props: {
        title: String,
        description: String
    },
    computed: {
        ...mapGetters('auth', [
            'isAuthLoading'
        ])
    },
    methods: {
        /**
         * Login Form Submit
         *
         * @param {String} formName The ref form name to be submitted
         * @returns void
         */
        submitForm: function (formName) {
            // validate the form
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.login()
                } else {
                    return false
                }
            })
        },

        /**
         * Login Action
         *
         * @returns void
         */
        login: async function () {
            // dispatch login action
            this.$store.dispatch('auth/login', this.authForm)
                .then((result) => {
                    // check if we have a redirect param
                    if (this.$router.history.current.query.redirect) {
                        // if so, push to that page
                        this.$router.push(this.$router.history.current.query.redirect)
                    } else {
                        // otherwise just go home
                        this.$router.push('/')
                    }
                })
                .catch((error) => {
                    // render error message
                    this.authError.title = error.response.statusText
                    this.authError.status = error.response.status
                    this.authError.message = error.response.data.data
                })
        }
    }
}
</script>

<style lang="scss">
@import 'Auth';
@import '@/scss/_components/_forms/form.base';
@import '@/scss/_components/_forms/_inputs/input.base';
</style>
