<template>
    <component
        :is="componentType"
        :href="this.href"
        :target="this.href ? '_blank' : ''"
        :type="this.href ? '' : this.type"
        @click="$emit('clicked')"
        :class="this.modifierClasses"
        :disabled="this.disabled">
        <template v-if="this.href">
            <span>
                <slot></slot>
            </span>
        </template>

        <template v-else>
            <slot></slot>
        </template>
    </component>
</template>

<script>
export default {
    name: 'Button',
    data () {
        return {}
    },
    props: {
        type: {
            type: String,
            required: false
        },
        inverted: {
            type: Boolean,
            required: false,
            default: false
        },
        size: {
            type: String,
            required: false
        },
        plain: {
            type: Boolean,
            required: false,
            default: false
        },
        classes: {
            type: String,
            required: false,
            default: ''
        },
        href: {
            type: String,
            required: false
        },
        disabled: {
            type: Boolean,
            required: false,
            default: false
        }
    },
    computed: {
        /**
         * Get component type
         *
         * @returns {String} The component name to use
         */
        componentType: function () {
            if (this.href) {
                return 'a'
            }

            return 'el-button'
        },

        /**
         * Computed list of modifier classes
         *
         * @returns {String} The list of modifier classes to apply
         */
        modifierClasses: function () {
            let modifierClasses = ''

            // Set the base class for <a> links
            if (this.href) {
                modifierClasses += 'el-button'
            }

            // Handle type prop, but only on <a> elements as the type is passed
            // as prop to <el-button> components directly
            if (this.type && this.href) {
                modifierClasses += ` el-button--${this.type}`
            }

            // Handle inverted prop
            if (this.inverted) {
                modifierClasses += ' el-button--light'
            }

            // Handle size prop
            if (this.size) {
                modifierClasses += ` el-button--${this.size}`
            }

            // Handle plain prop
            if (this.plain) {
                modifierClasses += ' is-plain'
            }

            // Handle class prop
            if (this.classes) {
                modifierClasses += ` ${this.classes}`
            }

            // Return additional classes string
            return modifierClasses
        }
    },
    methods: {
        handleButtonClick: function () {
            // Check if the passed route is number (i.e. -1)
            if (typeof this.route === 'number') {
                // If so trigger .go()
                return this.$router.go(this.route)
            }

            // Otherwise, assume it's a route string
            return this.$router.push(this.route)
        }
    }
}
</script>

<style lang="scss">
@import 'Button';
@import 'ButtonLink';
@import 'ButtonTransparent';
@import 'ButtonSettings';
</style>
