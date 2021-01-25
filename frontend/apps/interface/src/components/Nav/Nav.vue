<template>
    <div>
        <div class="el-nav" v-bind:class="this.classes">
            <div class="el-nav__left">
            </div>

            <div class="el-nav__right">
                <Button
                    type="transparent"
                    classes="el-nav__lang"
                    @clicked="languageSwitchVisible = true">
                    <Icon name="heroicons-translate"></Icon>
                    <span>{{ $t('lang.name') }}</span>
                </Button>

                <Button
                    type="transparent"
                    classes="el-nav__settings"
                    @clicked="$router.push('/settings')">
                    <Icon name="heroicons-cog"></Icon>
                </Button>

                <Button
                    v-if="isAuthenticated"
                    type="transparent"
                    classes="el-nav__logout"
                    @clicked="$router.push('/logout')">
                    <Icon name="heroicons-logout"></Icon>
                </Button>
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

import Button from '@/components/Button/Button'
import Icon from '@/components/Icons/Icon'
import LangSelectorDialog from '@/components/Dialogs/LangSelectorDialog.vue'

export default {
    name: 'Nav',
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
        Button,
        LangSelectorDialog
    },
    data () {
        return {
            online: null,
            languageSwitchVisible: false
        }
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
</style>
