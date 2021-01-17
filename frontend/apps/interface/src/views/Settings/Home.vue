<template>
    <div>
        <el-alert
            v-if="!this.$store.state.auth.required"
            :title="$t('settings-screen.auth.disabled.title')"
            :description="$t('settings-screen.auth.disabled.description')">
        </el-alert>

        <div class="el-section__group">
            <div class="el-section__content">
                <template v-for="(link, index) in this.links">
                    <el-button
                        v-if="link.internal"
                        :key="'settings-link-' + index"
                        @click="$router.push(link.path)"
                        type="settings el-button--block">
                        <span class="el-button__label">
                            <el-icon :name="link.icon"></el-icon>
                            {{ link.label }}
                        </span>

                        <el-icon name="heroicons-chevron-right"></el-icon>
                    </el-button>

                    <a
                        v-else
                        :key="'settings-link-' + index"
                        :href="link.url"
                        class="el-button el-button--settings el-button--block"
                        target="_blank" >
                        <span>
                            <span class="el-button__label">
                                <el-icon :name="link.icon"></el-icon>
                                {{ link.label }}
                            </span>

                            <el-icon name="heroicons-external-link"></el-icon>
                        </span>
                    </a>
                </template>
            </div>
        </div>

        <div class="el-section__footer">
            v{{ appVersion }}
        </div>
    </div>
</template>

<script>
import store from '@/store'

import LinksMixin from '@/mixins/links'

import ElAlert from '@/components/Alerts/Alert'
import ElIcon from '@/components/Icons/Icon'

export default {
    name: 'SettingsHome',
    mixins: [LinksMixin],
    components: {
        ElAlert,
        ElIcon
    },
    data () {
        return {
            links: [
                {
                    internal: true,
                    icon: 'heroicons-view-grid',
                    label: this.$t('settings-screen.components.title'),
                    path: '/settings/components'
                },
                {
                    internal: true,
                    icon: 'heroicons-translate',
                    label: this.$t('settings-screen.language.title'),
                    path: '/settings/language'
                },
                {
                    internal: false,
                    icon: 'heroicons-collection',
                    label: this.$t('settings-screen.filemanager.title'),
                    url: this.getExternalLink(this.$constants.FILEMANAGER, 'lang', true)
                },
                {
                    internal: true,
                    icon: 'heroicons-wifi',
                    label: this.$t('settings-screen.network.title'),
                    path: '/settings/network'
                },
                {
                    internal: true,
                    icon: 'heroicons-user',
                    label: this.$t('settings-screen.auth.title'),
                    path: '/settings/users'
                },
                {
                    internal: true,
                    icon: 'heroicons-server',
                    label: this.$t('settings-screen.system.title'),
                    path: '/settings/system'
                }
            ]
        }
    },
    computed: {
        appVersion: function () {
            return process.env.VUE_APP_VERSION
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

<style lang="scss"></style>
