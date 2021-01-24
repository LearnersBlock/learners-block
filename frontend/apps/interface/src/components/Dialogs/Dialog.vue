<template>
    <el-dialog
        :title="this.title"
        :visible.sync="dialogVisible">
        <slot name="content"></slot>
        <span
            v-if="this.$slots.footer"
            class="dialog-footer"
            slot="footer">
            <slot name="footer"></slot>
        </span>
    </el-dialog>
</template>

<script>
export default {
    name: 'Dialog',
    data () {
        return {
            selectedLang: this.$i18n.locale
        }
    },
    props: {
        title: {
            type: String,
            required: false
        },
        visible: {
            type: Boolean,
            required: true
        }
    },
    methods: {},
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
</style>
