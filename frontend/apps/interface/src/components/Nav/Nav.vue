<template>
    <div>
        <div class="el-nav" v-bind:class="this.classes">
            <div class="el-nav__left">
            </div>

            <div class="el-nav__right">
                <el-button
                    @click="languageSwitchVisible = true"
                    class="el-button--seamless el-nav__lang">
                    <Icon name="heroicons-translate"></Icon>
                    <span> {{ $t('lang.name') }} </span>
                </el-button>

                <el-button
                    @click="$router.push('/settings')"
                    class="el-button--seamless el-nav__settings">
                    <Icon name="heroicons-cog"></Icon>
                </el-button>

                <el-button
                    v-if="isAuthenticated"
                    @click="$router.push('/logout')"
                    class="el-button--seamless el-nav__logout">
                    <Icon name="heroicons-logout"></Icon>
                </el-button>
            </div>
        </div>

        <LangSelectorDialog
            :visible.sync="languageSwitchVisible"
            @hide-dialog="languageSwitchVisible = false">
        </LangSelectorDialog>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import Icon from '@/components/Icons/Icon'
import LangSelectorDialog from '@/components/Dialogs/LangSelectorDialog.vue'

export default {
    name: 'Nav',
    data () {
        return {
            online: null,
            languageSwitchVisible: false
        }
    },
    props: {
        type: {
            type: String,
            required: false
        },
        mode: {
            type: String,
            required: false
        }
    },
    components: {
        Icon,
        LangSelectorDialog
    },
    computed: {
        ...mapGetters('auth', [
            'isAuthenticated'
        ]),

        /**
         * Compute modifier classes
         *
         * @returns {String} The string of modifier classnames
         */
        classes: function () {
            let classes = ''

            // handle type
            if (this.type) {
                classes += 'el-nav--' + this.type
            }

            // handle mode
            if (this.mode) {
                classes += ' el-nav--' + this.mode
            }

            return classes
        }
    },
    methods: {
        /**
         * Bind dropdown actions to router
         */
        handleDropdownActions: function (command) {
            if (command === 'teacher-login') {
                this.$router.push({ path: '/login' })
            } else if (command === 'teacher-logout') {
                this.$router.push({ path: '/logout' })
            } else if (command === 'settings') {
                this.$router.push({ path: '/login' })
            }
        }
    }
}
</script>

<style lang="scss">
@import 'Nav.scss';

@import '@/scss/_components/_buttons/button.base';
@import '@/scss/_components/_buttons/button.icon';
@import '@/scss/_components/_buttons/button.seamless';
</style>
