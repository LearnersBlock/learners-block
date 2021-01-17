<template>
    <div class="el-header is-vertical" v-bind:class="this.classes">
        <div class="el-header__content">
            <div class="el-container is-vertical">
                <div class="el-header__nav">
                    <el-nav type="light" :mode="navMode ? navMode : ''"></el-nav>
                </div>

                <div class="el-header__inner" v-if="this.title">
                    <div
                        class="el-header__back"
                        :class="this.showBack ? '' : 'el-header__back--hidden'">
                        <button class="el-button el-button--link el-button--light" @click="$router.go(-1)">
                            <el-icon name="heroicons-arrow-narrow-left" type="light"></el-icon>
                            <span>{{ this.back }}</span>
                        </button>
                    </div>

                    <div class="el-header__content">
                        <div class="el-header__title" v-if="this.title">
                            <h1>{{ this.title }}</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="el-header__background">
            <ShapeOne />
            <ShapeTwo />
        </div>

        <div class="el-header__footer"></div>
    </div>
</template>

<script>
import ElNav from '@/components/Nav/Nav'
import ElIcon from '@/components/Icons/Icon'

import ShapeOne from '@/assets/shapes/blob-shape-01.svg'
import ShapeTwo from '@/assets/shapes/blob-shape-02.svg'

export default {
    name: 'Header',
    props: {
        title: String,
        back: String,
        showBack: Boolean,
        breadcrumbs: Array,
        navMode: String
    },
    components: {
        ElNav,
        ElIcon,
        ShapeOne,
        ShapeTwo
    },
    computed: {
        /**
         * Builds the additional classes based on the type & size props
         */
        classes: function () {
            let classes = ''

            // Handle type prop
            if (this.type) {
                classes += 'el-header--' + this.type
            }

            // Handle size prop
            if (this.size) {
                classes += ' el-header--' + this.size
            }

            // Return additional classes string
            return classes
        }
    }
}
</script>

<style scoped lang="scss">
@import 'header.scss';

@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.link';
</style>
