<template>
    <div>
        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.components.title') }}</h5>
            </div>

            <div class="el-section__content el-section__content--has-form">
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
            </div>
        </div>
    </div>
</template>

<script>
import settingsMixin from '@/mixins/settings'
import store from '@/store'

export default {
    name: 'SettingsComponents',
    components: {},
    mixins: [settingsMixin],
    data () {
        return {
            error: null
        }
    },
    computed: {
        fileviewerEnabled: {
            get () {
                return this.$store.state.settings.settings.components.fileviewer.active
            },
            set (value) {
                this.updateSetting('components.fileviewer', 'active', value)
            }
        },

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
