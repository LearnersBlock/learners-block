<template>
    <div class="el-section el-section--quicknav">
        <div class="el-container is-vertical">
            <div class="el-section__inner">
                <template v-for="(card, index) in this.items">
                    <el-card-link
                        v-if="card.enabled"
                        :key="index"
                        :label="card.label"
                        :link="card.link"
                        :icon="card.icon"
                        :color="card.color">
                    </el-card-link>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import ElCardLink from '@/components/Cards/CardLink.vue'

export default {
    name: 'QuickNav',
    data () {
        return {}
    },
    props: {
        items: {
            type: Array,
            required: true
        }
    },
    components: {
        ElCardLink
    },
    computed: {},
    methods: {}
}
</script>

<style lang="scss">
@import '@/scss/_components/_sections/section.base';
@import '@/scss/_components/_sections/section.quicknav';
</style>
