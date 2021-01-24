<template>
    <div
        role="alert"
        class="el-alert is-light"
        :class="this.classes">

        <Icon
            v-if="this.icon"
            :name="this.icon"
            :type="this.type">
        </Icon>

        <div class="el-alert__content">
            <span class="el-alert__title is-bold">
                {{ this.title }}
            </span>

            <p class="el-alert__description">
                {{ this.description }}
            </p>
        </div>
    </div>
</template>

<script>
import Icon from '@/components/Icons/Icon'

export default {
    name: 'Alert',
    components: {
        Icon
    },
    props: {
        type: {
            type: String,
            required: false,
            default: 'warning'
        },
        icon: {
            type: String,
            required: false,
            default: ''
        },
        title: {
            type: String,
            required: true
        },
        description: {
            type: String,
            required: true
        }
    },
    data () {
        return {}
    },
    computed: {
        classes: function () {
            // check if a type was passed as prop
            if (this.type) {
                // if so, return the alert type modifier
                return 'el-alert--' + this.type
            }

            return false
        }
    },
    methods: {}
}
</script>

<style lang="scss">
@import 'Alert.scss';
</style>
