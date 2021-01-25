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
        /**
         * Load the icon SVG dynamically
         *
         * @param   {String} name The icon name to load
         * @returns {Element} The icon's SVG to render
         */
        dynamicComponent: function () {
            return () => import(`@/assets/icons/${this.name}.svg`)
        },

        /**
         * Computed modifier classes based on the passed props
         *
         * @returns {String} The string of modifier classes for the icon
         */
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
