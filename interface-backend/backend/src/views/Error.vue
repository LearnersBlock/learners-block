<template>
    <div class="el-error">
        <div class="el-error__inner">
            <el-container direction="vertical">
                <div class="el-error__image">
                    <el-icon
                        name="streamline-icon-server-warning"
                        size="lg">
                    </el-icon>
                </div>

                <div class="el-error__title">
                    <h3>{{ this.page.title }}</h3>
                    <p>{{ this.page.description }}</p>
                </div>

                <div class="el-error__footer">
                    <el-button type="primary" v-on:click="this.goHome">{{
                    this.page.button }}</el-button>
                </div>
            </el-container>
        </div>
    </div>
</template>

<script>
import ElIcon from '@/components/Icons/Icon'

export default {
    name: 'Error',
    components: {
        ElIcon
    },
    data () {
        return {
            page: {
                title: '',
                description: '',
                button: ''
            }
        }
    },
    mounted () {
        if (this.$route.path === '/404') {
            this.page = this.$t('error-screen.404')
        } else {
            this.page = this.$t('error-screen.500')
        }
    },
    methods: {
        goHome: function () {
            this.$router.push('/')
        }
    }

}
</script>

<style lang="scss" scoped>
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_errors/error.base';
</style>
