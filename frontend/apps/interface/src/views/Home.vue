<template>
    <div>
        <Header :title="$t('home-screen.title')" />

        <Main>
            <Quicknav :items="this.quickNavItems" />
        </Main>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import store from '@/store'

import LinksMixin from '@/mixins/links'

import Header from '@/components/Header/Header.vue'
import Main from '@/components/Containers/Main.vue'
import Quicknav from '@/components/Quicknav/Quicknav.vue'

export default {
    name: 'Home',
    mixins: [LinksMixin],
    components: {
        Header,
        Main,
        Quicknav
    },
    data () {
        return {
            error: null
        }
    },
    computed: {
        ...mapState('settings', {
            settingsData: 'settings'
        }),

        quickNavItems () {
            return [
                {
                    label: this.$t('home-screen.quicknav.files.title'),
                    icon: 'collection',
                    color: 'orange',
                    link: {
                        internal: false,
                        path: this.getExternalLink(this.$constants.FILEMANAGER, 'lang')
                    },
                    enabled: this.settingsData.components.fileviewer.active
                },
                {
                    label: this.$t('home-screen.quicknav.website.title'),
                    icon: 'globe',
                    color: 'yellow',
                    link: {
                        internal: false,
                        path: this.$constants.WEBSITE
                    },
                    enabled: this.settingsData.components.website.active
                }
            ]
        }
    },
    beforeRouteEnter: async function (to, from, next) {
        try {
            await Promise.all([
                store.dispatch('settings/fetchSettings')
            ]).then(() => {
                next()
            })
        } catch (error) {
            next('/500')
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/_components/_main/main.base';
</style>
