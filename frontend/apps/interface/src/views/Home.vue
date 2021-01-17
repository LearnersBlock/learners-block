<template>
    <div>
        <el-header
            :title="$t('home-screen.title')">
        </el-header>

        <div class="el-main">
            <el-section-quicknav
                :items="this.quickNavItems">
            </el-section-quicknav>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import store from '@/store'

import LinksMixin from '@/mixins/links'

import ElHeader from '@/components/Header/Header.vue'
import ElSectionQuicknav from '@/components/Sections/Quicknav.vue'

export default {
    name: 'Home',
    mixins: [LinksMixin],
    components: {
        ElHeader,
        ElSectionQuicknav
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
