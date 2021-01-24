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
    data () {
        return {
            error: null
        }
    },
    computed: {
        /**
         * Back button
         *
         * Only show the back button if we're on settings sub-pages
         *
         * @returns void
         */
        showBackButton: function () {
            // if we're on the root settings page
            if (this.$route.path === '/settings') {
                // hide button
                return false
            }

            // otherwise, show the back button
            return true
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.settings';
</style>
