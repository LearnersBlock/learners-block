<template>
    <div>
        <div class="el-section__group">
            <div class="el-section__header">
                <h5>{{ $t('settings-screen.language.title') }}</h5>
            </div>

            <div class="el-section__content el-section__content--has-form">
                <el-form label-width="">
                    <el-form-item label="Default language" align="right">
                        <el-select v-model="defaultLanguage" placeholder="Select">
                            <el-option
                            v-for="lang in this.$i18n.availableLocales"
                            :key="lang"
                            :label="$t('lang.name', lang)"
                            :value="lang">
                            </el-option>
                        </el-select>
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
    name: 'SettingsLanguage',
    components: {},
    mixins: [settingsMixin],
    data () {
        return {
            error: null
        }
    },
    computed: {
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
