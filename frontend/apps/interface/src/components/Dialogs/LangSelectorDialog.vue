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
                    @change="updateLang"
                    border>
                    {{ $t('lang.name', lang) }}
                </el-radio>
            </template>
        </div>
    </el-dialog>
</template>

<script>
export default {
    name: 'LangSelectorDialog',
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
        /**
         * Method to update the stored language & hide the dialog
         *
         * @returns void
         */
        updateLang (newLang) {
            var self = this

            // Store new lang selection
            this.$store.dispatch('lang/updateLang', { lang: newLang, store: true })

            // Close dialog
            setTimeout(function () {
                self.$emit('hide-dialog', false)
            }, 150)
        }
    },
    computed: {
        /**
         * Identify if the dialog is visible or not
         *
         * @returns void
         */
        dialogVisible: {
            get () {
                return this.visible || false
            },

            set (newVal) {
                this.updateLang()
            }
        }
    },
    components: {}
}
</script>

<style lang="scss">
@import 'Dialog';
@import '@/scss/_components/_forms/_inputs/radio.base';
</style>
