<template>
    <div>
        <el-header
            :title="$t('settings-screen.title')"
            :back="$t('settings-screen.back')"
            :show-back="showBackButton"
            type="">
        </el-header>

        <div class="el-main">
            <div class="el-section el-section--settings">
                <div class="el-container is-vertical">
                    <div class="el-section__inner">
                        <transition :name="transitionName" mode="out-in">
                            <router-view></router-view>
                        </transition>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ElHeader from '@/components/Header/Header.vue'

const DEFAULT_TRANSITION = 'fade'

export default {
    name: 'Settings',
    components: {
        ElHeader
    },
    computed: {
        showBackButton: function () {
            if (this.$route.path === '/settings') {
                return false
            }

            return true
        }
    },
    data () {
        return {
            error: null,
            transitionName: DEFAULT_TRANSITION
        }
    },
    created: function () {
        this.$router.beforeEach((to, from, next) => {
            let transitionName = to.meta.transitionName || from.meta.transitionName

            if (transitionName === 'slide') {
                const toDepth = to.path.split('/').length
                const fromDepth = from.path.split('/').length
                transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left'
            }

            this.transitionName = transitionName || DEFAULT_TRANSITION

            next()
        })
    },
    beforeEach: function (to, from, next) {
        let transitionName = to.meta.transitionName || from.meta.transitionName

        if (transitionName === 'slide') {
            const toDepth = to.path.split('/').length
            const fromDepth = from.path.split('/').length
            transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left'
        }

        this.transitionName = transitionName

        next()
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_sections/section.base';
@import '@/scss/_components/_sections/section.settings';

@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.settings';
</style>
