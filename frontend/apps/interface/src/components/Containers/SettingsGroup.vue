<template>
    <div class="el-settings__group">
        <div class="el-settings__header">
            <slot name="title"></slot>
        </div>

        <div
            class="el-settings__content"
            v-loading="this.loading">
            <slot name="content"></slot>
        </div>

        <template slot></template>
    </div>
</template>

<script>
export default {
    name: 'SettingsGroupContainer',
    props: {
        loading: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    data () {
        return {}
    }
}
</script>

<style lang="scss">
</style>
