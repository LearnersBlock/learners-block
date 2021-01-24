<template>
    <div class="el-header is-vertical" v-bind:class="this.classes">
        <div class="el-header__content">
            <div class="el-container is-vertical">
                <div class="el-header__nav">
                    <Nav
                        type="light"
                        :mode="navMode ? navMode : ''">
                    </Nav>
                </div>

                <div class="el-header__inner" v-if="this.title">
                    <div
                        class="el-header__back"
                        :class="this.showBack ? '' : 'el-header__back--hidden'">

                        <button class="el-button el-button--link el-button--light" @click="$router.go(-1)">
                            <Icon
                                name="heroicons-arrow-narrow-left"
                                type="light">
                            </Icon>

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
import Nav from '@/components/Nav/Nav'
import Icon from '@/components/Icons/Icon'

import ShapeOne from '@/assets/shapes/blob-shape-01.svg'
import ShapeTwo from '@/assets/shapes/blob-shape-02.svg'

export default {
    name: 'Header',
    components: {
        Nav,
        Icon,
        ShapeOne,
        ShapeTwo
    },
    props: {
        title: {
            type: String,
            required: true
        },
        showBack: {
            type: Boolean,
            required: false,
            default: false
        },
        back: {
            type: String,
            required: (typeof showBack !== 'undefined')
        },
        breadcrumbs: {
            type: Array,
            required: false
        },
        size: {
            type: String,
            required: false
        },
        type: {
            type: String,
            required: false
        },
        navMode: {
            type: String,
            required: false
        }
    },
    data () {
        return {}
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
