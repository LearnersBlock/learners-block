<template>
    <div class="el-message">
        <div class="el-container is-vertical">
            <div class="el-message__inner">
                <div class="el-message__icon" v-if="this.icon">
                    <el-icon
                        :name="this.icon"
                        size="lg">
                    </el-icon>
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
import ElIcon from '@/components/Icons/Icon'

export default {
    name: 'Message',
    props: {
        icon: String
    },
    components: {
        ElIcon
    }
}
</script>

<style scoped lang="scss">
@import 'Message.scss';
</style>
