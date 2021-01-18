<template>
    <div>
        <div class="el-nav" v-bind:class="this.classes">
            <div class="el-nav__left">
            </div>

            <div class="el-nav__right">
                <el-button
                    @click="languageSwitchVisible = true"
                    class="el-button--seamless el-nav__lang">
                    <el-icon name="heroicons-translate"></el-icon>
                    <span> {{ $t('lang.name') }} </span>
                </el-button>

                <el-button
                    @click="$router.push('/settings')"
                    class="el-button--seamless el-nav__settings">
                    <el-icon name="heroicons-cog"></el-icon>
                </el-button>

                <el-button
                    v-if="isAuthenticated"
                    @click="$router.push('/logout')"
                    class="el-button--seamless el-nav__logout">
                    <el-icon name="heroicons-logout"></el-icon>
                </el-button>
            </div>
        </div>

        <el-lang-switcher-dialog
            :visible.sync="languageSwitchVisible"
            @hide-dialog="languageSwitchVisible = false">
        </el-lang-switcher-dialog>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'

import ElIcon from '@/components/Icons/Icon'
import ElLangSwitcherDialog from '@/components/Dialogs/LanguageSwitcher.vue'

export default {
    name: 'Nav',
    data () {
        return {
            online: null,
            languageSwitchVisible: false
        }
    },
    props: {
        type: String,
        mode: String
    },
    components: {
        ElIcon,
        ElLangSwitcherDialog
    },
    computed: {
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
        },

        ...mapGetters('auth', [
            'isAuthenticated'
        ])
    },
    mounted () {},
    methods: {
        handleDropdownActions: function (command) {
            if (command === 'teacher-login') {
                this.$router.push({ path: '/login' })
            } else if (command === 'teacher-logout') {
                this.$router.push({ path: '/logout' })
            } else if (command === 'settings') {
                this.$router.push({ path: '/login' })
            }
        },

        handleConnectivityChange: function (status) {
            this.online = status
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
