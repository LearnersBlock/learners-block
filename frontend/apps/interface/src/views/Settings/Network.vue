<template>
    <div>
        <SettingsGroupContainer :loading="this.wifi ? false : true">
                <template v-slot:title>
                    <h5>{{ $t('settings-screen.network.title') }}</h5>
                </template>

                <template v-slot:content>
                    <Button
                        type="settings"
                        size="block"
                        :href="getExternalLink($constants.WIFICONNECT, 'language')"
                        :disabled="isConnectButtonDisabled">
                        <span>
                            <Icon name="heroicons-wifi" />
                            {{ $t('settings-screen.network.connect.label') }}
                        </span>

                        <Icon name="heroicons-external-link" />
                    </Button>

                    <Button
                        type="settings"
                        size="block"
                        @clicked="openDialog(dialogData.warning)"
                        :disabled="isResetButtonDisabled">
                        <span>
                            <Icon name="heroicons-refresh" />
                            {{ $t('settings-screen.network.reset.label') }}
                        </span>

                        <Icon name="heroicons-chevron-right" />
                    </Button>
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
                            @clicked="resetWifiConnection()">
                            {{ button.label }}
                        </Button>
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
import Button from '@/components/Button/Button'
import Icon from '@/components/Icons/Icon'

export default {
    name: 'SettingsNetwork',
    mixins: [LinksMixin],
    components: {
        Icon,
        Dialog,
        Button,
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
                            size: 'half',
                            label: this.$t('general.cancel')
                        },
                        {
                            action: 'proceed',
                            type: 'danger',
                            size: 'half',
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
                            size: 'block',
                            label: this.$t('general.close')
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
                            size: 'block',
                            label: this.$t('general.close')
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
                return true
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

<style lang="scss"></style>
