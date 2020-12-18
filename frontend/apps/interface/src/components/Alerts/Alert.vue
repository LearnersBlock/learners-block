<template>
    <el-alert
        type="warning"
        :title="this.title"
        :description="this.description"
        :closable="false">
    </el-alert>
</template>
2
<script>
export default {
    name: 'Alert',
    components: {},
    data () {
        return {}
    },
    props: {
        title: String,
        description: String
    },
    computed: {},
    methods: {}
}
</script>

<style lang="scss">
@import '@/scss/_components/_alerts/alert.base';
</style>
