<template>
    <div>
        <div class="el-settings__group">
            <div class="el-settings__content">
                <template v-for="(link, index) in this.links">
                    <Button
                        v-if="link.internal"
                        :key="index"
                        type="settings"
                        size="block"
                        @clicked="$router.push(link.path)">
                        <span>
                            <Icon :name="link.icon" />
                            {{ link.label }}
                        </span>

                        <Icon name="heroicons-chevron-right" />
                    </Button>

                    <Button
                        v-else
                        :key="index"
                        type="settings"
                        size="block"
                        :href="link.url">
                        <span>
                            <Icon :name="link.icon" />
                            {{ link.label }}
                        </span>

                        <Icon name="heroicons-external-link" />
                    </Button>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import store from '@/store'

import LinksMixin from '@/mixins/links'

import Icon from '@/components/Icons/Icon'
import Button from '@/components/Button/Button'

export default {
    name: 'SettingsHome',
    mixins: [LinksMixin],
    components: {
        Icon,
        Button
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
