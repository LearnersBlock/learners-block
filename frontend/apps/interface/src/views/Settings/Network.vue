<template>
    <div>
        <SettingsGroupContainer :loading="this.wifi ? false : true">
                <template v-slot:title>
                    <h5>{{ $t('settings-screen.network.title') }}</h5>
                </template>

                <template v-slot:content>
                    <a
                        :href="getExternalLink($constants.WIFICONNECT, 'language')"
                        target="_blank"
                        class="el-button el-button--settings el-button--block"
                        :class="(isConnectButtonDisabled) ? 'is-disabled' : ''">
                        <span>
                            <span class="el-button__label">
                                <Icon name="heroicons-wifi"></Icon>
                                {{ $t('settings-screen.network.connect.label') }}
                            </span>

                            <Icon name="heroicons-external-link"></Icon>
                        </span>
                    </a>

                    <el-button
                        @click="openDialog(dialogData.warning)"
                        type="settings el-button--block"
                        :disabled="isResetButtonDisabled">
                        <span class="el-button__label">
                            <Icon name="heroicons-refresh"></Icon>
                            {{ $t('settings-screen.network.reset.label') }}
                        </span>

                        <Icon name="heroicons-chevron-right"></Icon>
                    </el-button>
                </template>
            </SettingsGroupContainer>

            <Dialog
                :title="dialogContent.title"
                :visible.sync="dialogVisible">
                <template v-slot:content>
                    <p v-html="dialogContent.content"></p>
                </template>

                <template v-slot:footer>
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
                            @click="resetWifiConnection()"
                            :key="index">
                            {{ button.label }}
                        </el-button>
                    </template>
                </template>
            </Dialog>
        </div>
</template>

<script>
import Api from '@/api/Api'

import LinksMixin from '@/mixins/links'

import SettingsGroupContainer from '@/components/Containers/SettingsGroup'
import Dialog from '@/components/Dialogs/Dialog'
import Icon from '@/components/Icons/Icon'

export default {
    name: 'SettingsNetwork',
    mixins: [LinksMixin],
    components: {
        Icon,
        Dialog,
        SettingsGroupContainer
    },
    data () {
        return {
            error: null,
            wifi: null,
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
                warning: {
                    title: this.$t('settings-screen.network.reset.warning.title'),
                    content: this.$t('settings-screen.network.reset.warning.content'),
                    buttons: [
                        {
                            action: 'close',
                            type: '',
                            class: 'el-button--half',
                            label: this.$t('settings-screen.network.reset.warning.cancel')
                        },
                        {
                            action: 'proceed',
                            type: 'danger',
                            class: 'el-button--half',
                            label: this.$t('settings-screen.network.reset.warning.submit')
                        }
                    ]
                },
                success: {
                    title: this.$t('settings-screen.network.reset.success.title'),
                    content: this.$t('settings-screen.network.reset.success.content'),
                    buttons: [
                        {
                            action: 'close',
                            type: '',
                            class: 'el-button--block',
                            label: this.$t('settings-screen.network.reset.success.close')
                        }
                    ]
                },
                error: {
                    title: this.$t('settings-screen.network.reset.error.title'),
                    content: this.$t('settings-screen.network.reset.error.content'),
                    buttons: [
                        {
                            action: 'close',
                            type: '',
                            class: 'el-button--block',
                            label: this.$t('settings-screen.network.reset.error.close')
                        }
                    ]
                }
            }
        }
    },
    computed: {
        /**
         * Check if Wifi Connect button should be disabled
         *
         * @returns {Boolean} Whether or not the button should be disabled
         */
        isConnectButtonDisabled: function () {
            if (this.wifi && (this.wifi === 'connected' || this.wifi === 'error')) {
                return true
            }

            return false
        },

        /**
         * Check if Wifi Reset button should be disabled
         *
         * @returns {Boolean} Whether or not the button should be disabled
         */
        isResetButtonDisabled: function () {
            if (this.wifi && (this.wifi === 'disconnected' || this.wifi === 'error')) {
                return false
            }

            return false
        }
    },
    methods: {
        /**
         * Open a dialog
         *
         * @param   {Object} data The dialog data to be rendered
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
         * Reset the Wifi connection
         *
         * @returns void
         */
        resetWifiConnection: function () {
            // Close warning modal
            this.dialogVisible = false

            // Loading state
            this.$store.commit('app/SET_LOADING', true)

            // Trigger API request
            Api()
                .post('/system/wifi/reset')
                .then((response) => {
                    console.log(response)
                    // Set loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // Cince the reset was successfull, invert the button active
                    // state manually
                    this.wifi = 'disconnected'

                    // Reset request was successful
                    this.openDialog(this.dialogData.success)
                })
                .catch((err) => {
                    // Reset request returned an error
                    console.error(err)  // eslint-disable-line

                    // Set loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // Reset request was unsuccessful
                    this.openDialog(this.dialogData.error)
                })
        }
    },
    mounted () {
        /**
         * Get WiFi connection status
         */
        Api()
            .get('/system/wifi/status')
            .then((response) => {
                // Ensure that we have the response we're looking for
                if (response.data && response.data.message) {
                    // Store response
                    this.wifi = response.data.message
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
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.secondary';
</style>
