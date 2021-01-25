<template>
    <main class="el-settings">
        <div class="el-container is-vertical">
            <div class="el-settings__inner">
                <Alert
                    v-if="!this.$store.state.auth.required"
                    :title="$t('settings-screen.auth.disabled.title')"
                    :description="$t('settings-screen.auth.disabled.description')">
                </Alert>

                <transition :name="transitionName" mode="out-in">
                    <router-view></router-view>
                </transition>
            </div>
        </div>
    </main>
</template>

<script>
import Alert from '@/components/Alerts/Alert'

const DEFAULT_TRANSITION = 'fade'

export default {
    name: 'SettingsContainer',
    components: {
        Alert
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
@import 'Settings';
</style>
