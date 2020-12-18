<template>
    <div class="el-auth">
        <div class="el-auth__inner" v-loading="this.isAuthLoading">
            <div class="el-auth__title">
                <h1>{{ this.title }}</h1>

                <p>{{ this.description }}</p>
            </div>

            <transition name="fade">
                <div v-show="authError.status" class="el-auth__error">
                    <div
                        role="alert"
                        class="el-alert el-alert--error is-light">
                        <el-icon name="heroicons-exclamation" type="danger"></el-icon>

                        <div class="el-alert__content">
                            <span class="el-alert__title is-bold">
                                {{ this.authError.title }}
                            </span>
                            <p class="el-alert__description">
                                {{ this.authError.message }}
                            </p>
                        </div>
                    </div>
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
                                <el-icon name="heroicons-user" type="light" classes="el-input__icon"></el-icon>
                            </i>
                        </el-input>
                    </el-form-item>

                    <el-form-item prop="password">
                        <el-input
                            type="password"
                            v-model="authForm.password"
                            :placeholder="$t('auth-screen.login.password')">
                            <i slot="prefix">
                                <el-icon name="heroicons-key" type="light" classes="el-input__icon"></el-icon>
                            </i>
                        </el-input>
                    </el-form-item>

                    <el-button
                        type="secondary"
                        @click="submitForm('authForm')"
                        class="el-button--block">
                        {{ $t('auth-screen.login.submit') }}
                    </el-button>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import ElIcon from '@/components/Icons/Icon'

export default {
    name: 'AuthLogin',
    components: {
        ElIcon
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
        submitForm: function (formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    this.login()
                } else {
                    return false
                }
            })
        },

        login: async function () {
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
                    this.authError.title = error.response.statusText
                    this.authError.status = error.response.status
                    this.authError.message = error.response.data.data
                })
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_forms/form.base';
@import '@/scss/_components/_forms/_inputs/input.base';
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.secondary';
@import '@/scss/_components/_alerts/alert.base';
@import '@/scss/_components/_auth/auth.base';
@import '@/scss/_components/_loading/loading.base';
</style>
