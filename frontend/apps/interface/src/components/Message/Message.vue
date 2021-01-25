<template>
    <div class="el-message">
        <div class="el-container is-vertical">
            <div class="el-message__inner">
                <div class="el-message__icon" v-if="this.icon">
                    <Icon
                        :name="this.icon"
                        size="lg">
                    </Icon>
                </div>

                <div class="el-message__title">
                    <slot name="title"></slot>
                </div>

                <div class="el-message__content">
                    <slot name="content"></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Icon from '@/components/Icons/Icon'

export default {
    name: 'Message',
    props: {
        icon: {
            type: String,
            required: false
        }
    },
    components: {
        Icon
    }
}
</script>

<style scoped lang="scss">
@import 'Message';
</style>
