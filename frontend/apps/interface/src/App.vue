<template>
    <div id="app" v-loading="this.$store.state.app.loading">
        <transition name="fade" mode="out-in" appear>
            <router-view />
        </transition>
    </div>
</template>

<script>
export default {
    name: 'App',
    components: {},
    data () {
        return {
            error: null
        }
    }
}
</script>

<style lang="scss">
@import '@/scss/main';

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition-duration: 0.25s;
  transition-property: height, opacity, transform;
  transition-timing-function: cubic-bezier(0.55, 0, 0.1, 1);
  overflow: hidden;
}

.slide-left-enter,
.slide-right-leave-active {
  opacity: 0;
  transform: translate(1rem, 0);
}

.slide-left-leave-active,
.slide-right-enter {
  opacity: 0;
  transform: translate(-1rem, 0);
}

.fade-enter-active, .fade-leave-active {
    transition: all .25s !important
}

.fade-enter, .fade-leave-to {
    opacity: 0 !important
}

.fade-enter-active {
    transition-delay: 0 !important
}

.fade-out-in-enter-active,
.fade-out-in-leave-active {
    transition: all .2s !important;
}

.fade-out-in-enter-active {
    transition-delay: .125s !important;
}

.fade-out-in-enter,
.fade-out-in-leave-to {
    opacity: 0 !important;
    transform: translateY(.25rem);
}

// .slide-leave-active,
// .slide-enter-active {
//     transition: all .5s !important;
// }

// .slide-enter-active {
//     transition-delay: 0 !important;
// }

// .slide-enter {
//     transform: translate(5rem, 0) !important;
// }
// .slide-leave-to {
//     opacity: 0;
//     transform: translate(-5rem, 0) !important;
// }
</style>
