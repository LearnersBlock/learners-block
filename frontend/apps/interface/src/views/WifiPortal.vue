<template>
    <div>
        <el-header />

        <div class="el-main">
        </div>
    </div>
</template>

<script>
import ElHeader from '@/components/Header/Header.vue'

export default {
    name: 'WifiPortal',
    components: {
        ElHeader
    },
    data () {
        return {
            error: null
        }
    },
    computed: {}
}
</script>

<style lang="scss">
@import '@/scss/_components/_main/main.base';
</style>
