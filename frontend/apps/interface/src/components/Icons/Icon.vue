<template>
    <i class="el-icon el-icon--svg" :class="componentClasses">
        <component :is="dynamicComponent"></component>
    </i>
</template>

<script>
export default {
    name: 'Icon',
    data () {
        return {}
    },
    props: {
        name: {
            type: String,
            required: true
        },
        type: {
            type: String,
            required: false
        },
        size: {
            type: String,
            required: false
        },
        classes: {
            type: String,
            required: false
        }
    },
    computed: {
        dynamicComponent: function () {
            return () => import(`@/assets/icons/${this.name}.svg`)
        },

        componentClasses: function () {
            let classes = ''

            if (this.type) {
                classes = classes.concat(classes, ' ', `el-icon--${this.type}`)
            }

            if (this.size) {
                classes = classes.concat(classes, ' ', `el-icon--${this.size}`)
            }

            if (this.classes) {
                classes = classes.concat(classes, ' ', this.classes)
            }

            return classes
        }
    }
}
</script>

<style lang="scss">
@import 'Icon';
</style>
