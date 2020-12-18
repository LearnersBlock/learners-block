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

import CommonsMixin from '@/mixins/commons'
import ComponentsMixin from '@/mixins/components'

import ElHeader from '@/components/Header/Header.vue'
import ElSectionQuicknav from '@/components/Sections/Quicknav.vue'

export default {
    name: 'Home',
    mixins: [CommonsMixin, ComponentsMixin],
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
                        path: this.getFileviewerLink()
                    },
                    enabled: this.settingsData.components.fileviewer.active
                },
                {
                    label: this.$t('home-screen.quicknav.website.title'),
                    icon: 'globe',
                    color: 'yellow',
                    link: {
                        internal: false,
                        path: this.settingsData.components.website.path
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
