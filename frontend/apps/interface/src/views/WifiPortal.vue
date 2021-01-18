<template>
    <div>
        <el-header navMode="restricted" />

        <el-message icon="streamline-icon-confetti">
            <template v-slot:title>
                <h3>{{ $t('wifiportal-screen.title') }}</h3>
            </template>

            <template v-slot:content>
                <p v-html="filteredMessageContent($t('wifiportal-screen.content'))"></p>
            </template>
        </el-message>
    </div>
</template>

<script>
import ElHeader from '@/components/Header/Header.vue'
import ElMessage from '@/components/Message/Message.vue'

export default {
    name: 'WifiPortal',
    components: {
        ElHeader,
        ElMessage
    },
    data () {
        return {
            error: null
        }
    },
    methods: {
        /**
         * Filters the message content to inject the frontend URL
         *
         * @param {String} content The content string to be filtered
         */
        filteredMessageContent: function (content) {
            // Build the frontend URL
            const frontendUrl = process.env.VUE_APP_API_BASE || location.origin

            // Replace it in the provided content string
            return content.replaceAll('%hostname%', frontendUrl)
        }
    }
}
</script>

<style lang="scss">
</style>
