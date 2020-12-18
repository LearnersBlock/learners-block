<template>
    <div class="el-card el-card--link is-linked" :class="cardColor">
        <div class="el-card__icon el-icon el-icon--svg el-icon--md">
            <el-icon-collection v-if="this.icon === 'collection'"></el-icon-collection>
            <el-icon-globe v-if="this.icon === 'globe'"></el-icon-globe>
        </div>

        <div class="el-card__header">
            <h2>{{ this.label }}</h2>
        </div>

        <div class="el-card__link">
            <router-link v-if="this.link.internal" :to="this.link.path"></router-link>
            <a v-else :href="this.link.path" target="_blank"></a>
        </div>
    </div>
</template>

<script>
import ElIconCollection from '@/assets/icons/heroicons-collection.svg'
import ElIconGlobe from '@/assets/icons/heroicons-globe.svg'

export default {
    name: 'CardLink',
    props: {
        label: {
            type: String,
            required: true
        },
        link: {
            type: Object,
            required: true
        },
        icon: {
            type: String,
            required: true
        },
        color: {
            type: String,
            required: false
        }
    },
    computed: {
        cardColor () {
            if (this.color) {
                return `el-card--${this.color}`
            }

            return null
        }
    },
    components: {
        ElIconCollection,
        ElIconGlobe
    }
}
</script>

<style scoped lang="scss">
@import '@/scss/_components/_cards/card.base';
@import '@/scss/_components/_cards/card.link';
</style>
