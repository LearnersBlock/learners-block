<template>
    <div>
        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.system.hostname.title') }}</h5>
            </div>

            <div class="el-section__content">
                <el-form ref="hostnameSettings" :model="hostnameSettings"
                :rules="hostnameSettingsRules" label-width="" :status-icon="true">
                    <el-form-item label="" align="right" prop="hostname">
                        <el-input v-model="hostnameSettings.hostname">
                            <template slot="prepend">http://</template>
                            <template slot="append">
                                {{ this.$store.state.settings.settings.system.tld || '.local' }}
                            </template>
                        </el-input>
                    </el-form-item>

                    <el-button
                        @click="updateHostname()"
                        type=" el-button--block"
                        :disabled="hostnameSubmitDisabled"
                        plain>
                        {{ $t('settings-screen.system.hostname.update.label') }}
                    </el-button>
                </el-form>
            </div>
        </div>

        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.system.database.title') }}</h5>
            </div>

            <div class="el-section__content">
                <el-button
                    @click="resetDatabase()"
                    type="danger el-button--block"
                    plain>
                    {{ $t('settings-screen.system.database.reset.label') }}
                </el-button>
            </div>
        </div>

        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.system.versions.title') }}</h5>
            </div>

            <div class="el-section__content">
                <el-table
                    :data="this.versions"
                    :show-header="false"
                    style="width: 100%">
                    <el-table-column
                        prop="id"
                        name="Component"
                        :formatter="getComponentName">
                    </el-table-column>
                    <el-table-column
                        prop="version"
                        name="Version"
                        align="right">
                    </el-table-column>
                </el-table>
            </div>
        </div>

        <el-dialog
            :title="dialogContent.title"
            :visible.sync="dialogVisible">
            <p v-html="dialogContent.content"></p>
            <span
                v-if="dialogContent.buttons.length"
                class="dialog-footer"
                slot="footer">
                <template v-for="(button, index) in dialogContent.buttons">
                    <el-button
                        v-if="button.action === 'close'"
                        :type="button.type"
                        :class="button.class"
                        @click="dialogVisible = false"
                        :key="index">
                        {{ button.label }}
                    </el-button>

                    <el-button
                        v-if="button.action === 'proceed'"
                        :type="button.type"
                        :class="button.class"
                        @click="resetDatabase()"
                        :key="index">
                        {{ button.label }}
                    </el-button>
                </template>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import Api from '@/api/Api'

import settingsMixin from '@/mixins/settings'
import store from '@/store'

import debounce from 'lodash/debounce'

export default {
    name: 'SettingsNetwork',
    components: {},
    mixins: [settingsMixin],
    data () {
        const validateHostname = (rule, value, callback) => {  // eslint-disable-line
            // make sure we have a value to check
            if (!value) {
                // if not, return error
                return callback(new Error('Please input a hostname'))
            }

            // prepare regex for allowed chars
            const specialCharsRegex = new RegExp(/^[a-zA-Z0-9-_]*$/)

            // run the regex test
            if (specialCharsRegex.test(value)) {
                // if it passes, approve the hostname
                callback()
            } else {
                // otherwise, throw an error
                callback(new Error('Hostname contains invalid characters.'))
            }
        }

        return {
            error: null,
            versions: null,
            hostnameSubmitDisabled: true,
            hostnameSettings: {
                hostname: this.$store.state.settings.settings.system.hostname || window.location.hostname
            },
            hostnameSettingsRules: {
                hostname: [
                    { validator: validateHostname, trigger: 'blur' },
                    { required: true, message: '', trigger: 'blur' },
                    { min: 2, max: 30, message: '', trigger: 'blur' }
                ]
            },
            dialogVisible: false,
            dialogContent: {
                title: null,
                content: null,
                buttons: [
                    {
                        action: null,
                        type: null,
                        class: null,
                        label: null
                    }
                ]
            },
            dialogData: {
                hostname: {
                    success: {
                        title: this.$t('settings-screen.system.hostname.update.success.title'),
                        content: this.$t('settings-screen.system.hostname.update.success.content'),
                        buttons: [
                            {
                                action: 'close',
                                type: '',
                                class: 'el-button--block',
                                label: this.$t('settings-screen.system.hostname.update.success.close')
                            }
                        ]
                    },
                    error: {
                        title: this.$t('settings-screen.system.hostname.update.error.title'),
                        content: this.$t('settings-screen.system.hostname.update.error.content'),
                        buttons: [
                            {
                                action: 'close',
                                type: '',
                                class: 'el-button--block',
                                label: this.$t('settings-screen.system.hostname.update.error.close')
                            }
                        ]
                    }
                },
                database: {
                    success: {
                        title: this.$t('settings-screen.system.database.reset.success.title'),
                        content: this.$t('settings-screen.system.database.reset.success.content'),
                        buttons: [
                            {
                                action: 'close',
                                type: '',
                                class: 'el-button--block',
                                label: this.$t('settings-screen.system.database.reset.success.close')
                            }
                        ]
                    },
                    error: {
                        title: this.$t('settings-screen.system.database.reset.error.title'),
                        content: this.$t('settings-screen.system.database.reset.error.content'),
                        buttons: [
                            {
                                action: 'close',
                                type: '',
                                class: 'el-button--block',
                                label: this.$t('settings-screen.system.database.reset.error.close')
                            }
                        ]
                    }
                }
            }
        }
    },
    mounted () {
        // get the component versions
        Api()
            .get('/system/info')
            .then((response) => {
                if (response.data && response.data) {
                    this.versions = response.data.versions || null
                }
            })
            .catch((err) => {
                // if the backend returned a proper error response
                if (err.response && err.response.data && err.response.data.connection) {
                    // update wifi status
                    this.wifi = err.response.data.connection
                } else {
                    // otherwise, force error state
                    this.wifi = 'error'
                }
            })
    },
    computed: {},
    methods: {
        getComponentName: function (row, column) {
            return this.$t('settings-screen.system.versions.components.' + row.id) || row.id
        },

        updateHostname: function () {
            // loading state
            this.$store.commit('app/SET_LOADING', true)

            // revalidate the form
            this.$refs.hostnameSettings.validate((valid) => {
                // if the hostname is valid
                if (valid) {
                    Api()
                        .patch('/system/hostname', { ...this.hostnameSettings })
                        .then((response) => {
                            // loading state
                            this.$store.commit('app/SET_LOADING', false)

                            // copy dialog data in case the user re-changes the
                            // hostname without reloading the page
                            const dialogData = { ...this.dialogData.hostname.success }

                            // update dialog content with hostname and SSID
                            dialogData.content = dialogData.content.replaceAll('%hostname%', response.data.hostname)
                            dialogData.content = dialogData.content.replaceAll('%ssid%', response.data.ssid)

                            // update the database
                            this.updateSetting('system', 'hostname', response.data.hostname)

                            // reset request was successful
                            this.openDialog(dialogData)
                        })
                        .catch((err) => {
                            // reset request returned an error
                            console.error(err) // eslint-disable-line

                            // change hostname back to original
                            this.hostnameSettings.hostname = store.state.settings.settings.system.hostname

                            // loading state
                            this.$store.commit('app/SET_LOADING', false)

                            // reset request was successful
                            this.openDialog(this.dialogData.hostname.error)
                        })
                } else {
                    // loading state
                    this.$store.commit('app/SET_LOADING', false)

                    return false
                }
            })
        },

        checkHostnameValidity: debounce(function () {
            // remove spaces at the end of the string
            this.hostnameSettings.hostname = this.hostnameSettings.hostname.trim()

            // run validator
            this.$refs.hostnameSettings.validate((valid) => {
                if (valid) {
                    // if the hostname is valid, check that it's the same as the
                    // current one to prevent triggering uneccessary updates
                    if (this.hostnameSettings.hostname === store.state.settings.settings.system.hostname) {
                        // if they are identical, keep the button disabled
                        this.hostnameSubmitDisabled = true
                    } else {
                        // otherwise, enable it
                        this.hostnameSubmitDisabled = false
                    }
                } else {
                    // otherwise, if the hostname is not valid, keep the button disabled
                    this.hostnameSubmitDisabled = true
                    return false
                }
            })
        }, 400),

        openDialog: function (data) {
            setTimeout(() => {
                // update dialog content
                this.dialogContent = data

                // show dialog
                this.dialogVisible = true
            }, 450)
        },

        resetDatabase: function () {
            // close warning modal
            this.dialogVisible = false

            // loading state
            this.$store.commit('app/SET_LOADING', true)

            // trigger API request
            Api()
                .post('/system/database/reset')
                .then((response) => {
                    // loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // reset request was successful
                    this.openDialog(this.dialogData.database.success)
                })
                .catch((err) => {
                    // reset request returned an error
                    console.error(err) // eslint-disable-line

                    // loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // reset request was successful
                    this.openDialog(this.dialogData.database.error)
                })
        }
    },
    watch: {
        'hostnameSettings.hostname': function (newVal, oldVal) {
            this.checkHostnameValidity()
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
@import '@/scss/_components/_tables/table.base';
@import '@/scss/_components/_forms/form.base';
// @import '@/scss/_components/_dialogs/dialog.base';
</style>
