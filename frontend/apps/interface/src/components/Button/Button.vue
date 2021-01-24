<template>
    <div>
        <template v-if="!this.href">
            <el-button
                v-if="link.internal"
                :key="index"
                @click="$router.push(this.route)"
                type="settings el-button--block">
                <slot></slot>
            </el-button>
        </template>

        <templater v-else>
            <a
                :href="this.href"
                class="el-button el-button--settings el-button--block"
                target="_blank">
                <slot></slot>
            </a>
        </templater>


        <el-button
            v-if="link.internal"
            :key="index"
            @click="$router.push(link.path)"
            type="settings el-button--block">
        </el-button>

        <a
            v-else
            :key="index"
            :href="link.url"
            class="el-button el-button--settings el-button--block"
            target="_blank">
        </a>
    </div>
</template>

<script>
export default {
    name: 'Main',
    data () {
        return {}
    },
    props: {},
    computed: {
        classes: function () {
            let classes = ''

            // // handle type
            // if (this.type) {
            //     classes += 'el-nav--' + this.type
            // }

            // // handle mode
            // if (this.mode) {
            //     classes += ' el-nav--' + this.mode
            // }

            return classes
        }
    },
}
</script>

<style lang="scss">
@import 'Main.scss';
</style>
