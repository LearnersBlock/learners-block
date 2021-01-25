<template>
    <div>
        <SettingsGroupContainer>
                <template v-slot:title>
                    <h5>{{ $t('settings-screen.system.hostname.title') }}</h5>
                </template>

                <template v-slot:content>
                    <el-form ref="hostnameSettings" :model="hostnameSettings"
                    :rules="hostnameSettingsRules" label-width="" :status-icon="true">
                        <el-form-item label="" align="right" prop="hostname">
                            <el-input v-model="hostnameSettings.hostname">
                                <template slot="prepend">http://</template>
                                <template slot="append">
                                    {{ $store.state.settings.settings.system.tld || '.local' }}
                                </template>
                            </el-input>
                        </el-form-item>

                        <Button
                            type="primary"
                            size="block"
                            :plain="true"
                            @clicked="updateHostname()"
                            :disabled="hostnameSubmitDisabled">
                            {{ $t('settings-screen.system.hostname.update.label') }}
                        </Button>
                    </el-form>
                </template>
        </SettingsGroupContainer>

        <SettingsGroupContainer>
            <template v-slot:title>
                <h5>{{ $t('settings-screen.system.database.title') }}</h5>
            </template>

            <template v-slot:content>
                <Button
                    type="danger"
                    size="block"
                    :plain="true"
                    @clicked="resetDatabase()">
                    {{ $t('settings-screen.system.database.reset.label') }}
                </Button>
            </template>
        </SettingsGroupContainer>

        <SettingsGroupContainer>
            <template v-slot:title>
                <h5>{{ $t('settings-screen.system.versions.title') }}</h5>
            </template>

            <template v-slot:content>
                <el-table
                    :data="versions"
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
            </template>
        </SettingsGroupContainer>

        <Dialog
            :title="dialogContent.title"
            :visible.sync="dialogVisible">
            <template v-slot:content>
                <p v-html="dialogContent.content"></p>
            </template>

            <template v-slot:footer v-if="dialogContent.buttons.length">
                <template v-for="(button, index) in dialogContent.buttons">
                    <Button
                        v-if="button.action === 'close'"
                        :key="index"
                        :type="button.type"
                        :size="button.size"
                        @clicked="dialogVisible = false">
                        {{ button.label }}
                    </Button>

                    <Button
                        v-if="button.action === 'proceed'"
                        :key="index"
                        :type="button.type"
                        :size="button.size"
                        @clicked="resetDatabase()">
                        {{ button.label }}
                    </Button>
                </template>
            </template>
        </Dialog>
    </div>
</template>

<script>
import Api from '@/api/Api'

import settingsMixin from '@/mixins/settings'
import store from '@/store'

import debounce from 'lodash/debounce'

import SettingsGroupContainer from '@/components/Containers/SettingsGroup'
import Dialog from '@/components/Dialogs/Dialog'
import Button from '@/components/Button/Button'

export default {
    name: 'NetworkSettings',
    mixins: [settingsMixin],
    components: {
        SettingsGroupContainer,
        Dialog,
        Button
    },
    data () {
        /**
         * Hostname validation
         *
         * @returns {Function} Validation callback
         */
        const validateHostname = (rule, value, callback) => {  // eslint-disable-line
            // Make sure we have a value to check
            if (!value) {
                // If not, return error
                return callback(new Error('Please input a hostname'))
            }

            // Prepare regex for allowed chars
            const specialCharsRegex = new RegExp(/^[a-zA-Z0-9-_]*$/)

            // Run the regex test
            if (specialCharsRegex.test(value)) {
                // If it passes, approve the hostname
                callback()
            } else {
                // Otherwise, throw an error
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
                                size: 'block',
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
                                size: 'block',
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
                                size: 'block',
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
                                size: 'block',
                                label: this.$t('settings-screen.system.database.reset.error.close')
                            }
                        ]
                    }
                }
            }
        }
    },
    methods: {
        /**
         * Get the human-readable component name for the version list
         *
         * @param   {Object} row    The row data from a table
         * @param   {String} row.id The component ID to retrieve the name for
         * @returns {String} The component name
         */
        getComponentName: function (row, column) {
            return this.$t('settings-screen.system.versions.components.' + row.id) || row.id
        },

        /**
         * Update the device hostname
         *
         * @returns void
         */
        updateHostname: function () {
            // Set loading state
            this.$store.commit('app/SET_LOADING', true)

            // Revalidate the form
            this.$refs.hostnameSettings.validate((valid) => {
                // If the hostname is valid
                if (valid) {
                    // Trigger API call
                    Api()
                        .patch('/system/hostname', { ...this.hostnameSettings })
                        .then((response) => {
                            // Set loading state
                            this.$store.commit('app/SET_LOADING', false)

                            // Copy dialog data in case the user re-changes the
                            // hostname without reloading the page
                            const dialogData = { ...this.dialogData.hostname.success }

                            // Ipdate dialog content with hostname and SSID
                            dialogData.content = dialogData.content.replaceAll('%hostname%', response.data.hostname)
                            dialogData.content = dialogData.content.replaceAll('%ssid%', response.data.ssid)

                            // Update the database
                            this.updateSetting('system', 'hostname', response.data.hostname)

                            // Reset request was successful
                            this.openDialog(dialogData)
                        })
                        .catch((err) => {
                            // Reset request returned an error
                            console.error(err) // eslint-disable-line

                            // Change hostname back to original
                            this.hostnameSettings.hostname = store.state.settings.settings.system.hostname

                            // Set loading state
                            this.$store.commit('app/SET_LOADING', false)

                            // Reset request was successful
                            this.openDialog(this.dialogData.hostname.error)
                        })
                } else {
                    // If hostname is invalid, yet passed validation
                    // Set loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // And abort
                    return false
                }
            })
        },

        /**
         * Check the hostname validity
         *
         * @returns {Boolean} Whether the hostname is valid or not
         */
        checkHostnameValidity: debounce(function () {
            // Remove spaces at the end of the string
            this.hostnameSettings.hostname = this.hostnameSettings.hostname.trim()

            // Run validator
            this.$refs.hostnameSettings.validate((valid) => {
                if (valid) {
                    // If the hostname is valid, check that it's the same as the
                    // current one to prevent triggering uneccessary updates
                    if (this.hostnameSettings.hostname === store.state.settings.settings.system.hostname) {
                        // If they are identical, keep the button disabled
                        this.hostnameSubmitDisabled = true
                    } else {
                        // Otherwise, enable it
                        this.hostnameSubmitDisabled = false
                    }
                } else {
                    // Otherwise, if the hostname is not valid, keep the button disabled
                    this.hostnameSubmitDisabled = true
                    return false
                }
            })
        }, 400),

        /**
         * Opens a dialog
         *
         * @returns void
         */
        openDialog: function (data) {
            setTimeout(() => {
                // Set the dialog content
                this.dialogContent = data

                // Show the dialog
                this.dialogVisible = true
            }, 450)
        },

        /**
         * Reset database
         *
         * @returns void
         */
        resetDatabase: function () {
            // Close warning modal
            this.dialogVisible = false

            // Set loading state
            this.$store.commit('app/SET_LOADING', true)

            // Trigger API request
            Api()
                .post('/system/database/reset')
                .then((response) => {
                    // Set loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // Reset request was successful
                    this.openDialog(this.dialogData.database.success)
                })
                .catch((err) => {
                    // Reset request returned an error
                    console.error(err) // eslint-disable-line

                    // Set loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // Reset request was successful
                    this.openDialog(this.dialogData.database.error)
                })
        }
    },
    mounted () {
        /**
         * Fetch system info from API
         */
        Api()
            .get('/system/info')
            .then((response) => {
                if (response.data && response.data) {
                    // Set versions
                    this.versions = response.data.versions || null

                    // Set storage
                    // @TODO
                }
            })
            .catch((err) => {
                // If the backend returned a proper error response
                if (err.response && err.response.data && err.response.data.connection) {
                    // Update wifi status
                    this.wifi = err.response.data.connection
                } else {
                    // Otherwise, force error state
                    this.wifi = 'error'
                }
            })
    },
    watch: {
        // Automatically re-validate hostname on change
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
</style>
