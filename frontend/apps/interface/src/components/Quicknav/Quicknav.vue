<template>
    <div class="el-quicknav" v-if="this.items">
        <div class="el-container is-vertical">
            <div class="el-quicknav__inner">
                <template v-for="(card, index) in this.items">
                    <div
                        v-if="card.enabled"
                        :key="`qn-${index}`"
                        class="el-quicknav__item"
                        :class="getColorClass(card.color)">
                        <div class="el-quicknav__icon">
                            <Icon :name="card.icon" size="md" />
                        </div>

                        <div class="el-quicknav__header">
                            <h2>{{ card.label }}</h2>
                        </div>

                        <div class="el-quicknav__link">
                            <router-link v-if="card.link.internal" :to="card.link.path"></router-link>
                            <a v-else :href="card.link.path" target="_blank"></a>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import Icon from '@/components/Icons/Icon'

export default {
    name: 'LinkCard',
    props: {
        items: {
            type: Array,
            required: true
        }
    },
    components: {
        Icon
    },
    data () {
        return {}
    },
    methods: {
        /**
         * Computes the component modifier classes
         *
         * @param   {String} color The color name to use for the component (opt.)
         * @returns {String|Null} The string of modifier classes to apply
         */
        getColorClass (color = null) {
            // Handle color prop
            if (color) {
                return `el-quicknav__item--${color}`
            }

            return null
        }
    }
}
</script>

<style lang="scss">
@import 'Quicknav.scss';
</style>
