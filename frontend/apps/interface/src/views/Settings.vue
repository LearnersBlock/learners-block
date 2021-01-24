<template>
    <div>
        <Header
            :title="$t('settings-screen.title')"
            :back="$t('settings-screen.back')"
            :show-back="showBackButton"
            type=""
        />

        <SettingsContainer />
    </div>
</template>

<script>
import Header from '@/components/Header/Header'
import SettingsContainer from '@/components/Containers/Settings'

export default {
    name: 'Settings',
    components: {
        Header,
        SettingsContainer
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
            error: null
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.settings';
</style>
