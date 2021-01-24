<template>
    <div>
        <Header navMode="restricted" />

        <Message icon="streamline-icon-confetti">
            <template v-slot:title>
                <h3>{{ $t('wifiportal-screen.title') }}</h3>
            </template>

            <template v-slot:content>
                <p v-html="filteredMessageContent($t('wifiportal-screen.content'))"></p>
            </template>
        </Message>
    </div>
</template>

<script>
import Header from '@/components/Header/Header.vue'
import Message from '@/components/Message/Message.vue'

export default {
    name: 'WifiPortal',
    components: {
        Header,
        Message
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
