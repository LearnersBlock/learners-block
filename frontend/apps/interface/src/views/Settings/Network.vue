<template>
    <div>
        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.network.title')}}</h5>
            </div>

            <div class="el-section__content" v-loading="this.wifi ? false : true">
                <a
                    href="/wifi/connect"
                    target="_blank"
                    class="el-button el-button--settings el-button--block"
                    :class="(isConnectButtonDisabled) ? 'is-disabled' : ''">
                    <span>
                        <span class="el-button__label">
                            <el-icon name="heroicons-wifi"></el-icon>
                            {{ $t('settings-screen.network.connect.label') }}
                        </span>

                        <el-icon name="heroicons-external-link"></el-icon>
                    </span>
                </a>

                <el-button
                    @click="openDialog(dialogData.warning)"
                    type="settings el-button--block"
                    :disabled="isResetButtonDisabled">
                    <span class="el-button__label">
                        <el-icon name="heroicons-refresh"></el-icon>
                        {{ $t('settings-screen.network.reset.label') }}
                    </span>

                    <el-icon name="heroicons-chevron-right"></el-icon>
                </el-button>
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
                        @click="resetWifiConnection()"
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

import ElIcon from '@/components/Icons/Icon'

export default {
    name: 'SettingsNetwork',
    components: {
        ElIcon
    },
    mixins: [],
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
        isConnectButtonDisabled: function () {
            if (this.wifi && (this.wifi === 'connected' || this.wifi === 'error')) {
                return true
            }

            return false
        },

        isResetButtonDisabled: function () {
            if (this.wifi && (this.wifi === 'disconnected' || this.wifi === 'error')) {
                return true
            }

            return false
        }
    },
    mounted () {
        // get the wifi connection status to toggle the button logic
        Api()
            .get('/system/wifi/status')
            .then((response) => {
                if (response.data && response.data.connection) {
                    this.wifi = response.data.connection
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
    methods: {
        openDialog: function (data) {
            setTimeout(() => {
                // update dialog content
                this.dialogContent = data

                // show dialog
                this.dialogVisible = true
            }, 450)
        },

        resetWifiConnection: function () {
            // close warning modal
            this.dialogVisible = false

            // loading state
            this.$store.commit('app/SET_LOADING', true)

            // trigger API request
            Api()
                .post('/system/wifi/reset')
                .then((response) => {
                    // loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // since the reset was successfull, invert the button active
                    // state manually
                    this.wifi = 'disconnected'

                    // reset request was successful
                    this.openDialog(this.dialogData.success)
                })
                .catch((err) => {
                    // reset request returned an error
                    console.error(err)  // eslint-disable-line

                    // loading state
                    this.$store.commit('app/SET_LOADING', false)

                    // reset request was successful
                    this.openDialog(this.dialogData.error)
                })
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_dialogs/dialog.base';
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.secondary';
</style>
