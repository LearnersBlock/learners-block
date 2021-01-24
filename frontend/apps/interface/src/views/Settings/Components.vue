<template>
    <SettingsGroupContainer>
        <template v-slot:title>
            <h5>{{ $t('settings-screen.components.title') }}</h5>
        </template>

        <template v-slot:content>
            <el-form label-width="">
                <el-form-item
                    :label="$t('settings-screen.components.fileviewer.label')"
                    class="el-form-item--bordered"
                    align="right">
                    <el-switch
                        v-model="fileviewerEnabled">
                    </el-switch>
                </el-form-item>

                <el-form-item
                    :label="$t('settings-screen.components.website.label')"
                    class="el-form-item--bordered"
                    align="right">
                    <el-switch
                        v-model="websiteEnabled">
                    </el-switch>
                </el-form-item>
            </el-form>
        </template>
    </SettingsGroupContainer>
</template>

<script>
import settingsMixin from '@/mixins/settings'
import store from '@/store'

import SettingsGroupContainer from '@/components/Containers/SettingsGroup'

export default {
    name: 'ComponentSettings',
    mixins: [settingsMixin],
    components: {
        SettingsGroupContainer
    },
    data () {
        return {
            error: null
        }
    },
    computed: {
        /**
         * Check if fileviewer component is enabled
         *
         * @returns {Boolean} Return true or false depending on component setting
         */
        fileviewerEnabled: {
            get () {
                return this.$store.state.settings.settings.components.fileviewer.active
            },
            set (value) {
                this.updateSetting('components.fileviewer', 'active', value)
            }
        },

        /**
         * Check if website component is enabled
         *
         * @returns {Boolean} Return true or false depending on component setting
         */
        websiteEnabled: {
            get () {
                return this.$store.state.settings.settings.components.website.active
            },
            set (value) {
                this.updateSetting('components.website', 'active', value)
            }
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
@import '@/scss/_components/_forms/_inputs/switch.base';
</style>
