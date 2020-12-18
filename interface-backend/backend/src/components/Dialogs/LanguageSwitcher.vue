<template>
    <el-dialog
        :title="$t('lang.selector.title')"
        :visible.sync="dialogVisible"
        :show-close="true">

        <div>
            <template v-for="(lang, index) in this.$i18n.availableLocales">
                <el-radio
                    :key="'lang-' + index"
                    v-model="$i18n.locale"
                    :label="lang"
                    @change="hideDialog"
                    border>
                    {{ $t('lang.name', lang) }}
                </el-radio>
            </template>
        </div>
    </el-dialog>
</template>

<script>
export default {
    name: 'LangSwitcherDialog',
    data () {
        return {
            selectedLang: this.$i18n.locale
        }
    },
    props: {
        visible: {
            type: Boolean,
            required: true
        }
    },
    methods: {
        hideDialog (newLang) {
            var self = this

            // store new lang selection
            this.$store.dispatch('lang/updateLang', { lang: newLang, store: true })

            // close dialog
            setTimeout(function () {
                self.$emit('hide-dialog', false)
            }, 150)
        }
    },
    computed: {
        dialogVisible: {
            get () {
                return this.visible || false
            },

            set (newVal) {
                this.hideDialog()
            }
        }
    },
    components: {}
}
</script>

<style lang="scss">
@import '@/scss/_components/_dialogs/dialog.base';
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.secondary';
@import '@/scss/_components/_forms/_inputs/radio.base';
</style>
