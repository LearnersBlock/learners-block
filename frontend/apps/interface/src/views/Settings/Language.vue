<template>
    <SettingsGroupContainer>
        <template v-slot:title>
            <h5>{{ $t('settings-screen.language.title') }}</h5>
        </template>

        <template v-slot:content>
            <el-form label-width="">
                <el-form-item label="Default language" align="right">
                    <el-select v-model="defaultLanguage" placeholder="Select">
                        <el-option
                            v-for="lang in $i18n.availableLocales"
                            :key="lang"
                            :label="$t('lang.name', lang)"
                            :value="lang">
                        </el-option>
                    </el-select>
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
    name: 'SettingsLanguage',
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
         * Get the default language from the settings
         *
         * @returns {String} The stored default language code, falls back to current
         */
        defaultLanguage: {
            get () {
                return this.$store.state.settings.settings.lang.default || this.$i18n.locale
            },
            set (value) {
                this.updateSetting('lang', 'default', value)
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
@import '@/scss/_components/_forms/_inputs/select.base';
</style>
