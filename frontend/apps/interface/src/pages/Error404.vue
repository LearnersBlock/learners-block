<template>
  <div class="fullscreen bg-primary text-white text-center q-pa-md flex flex-center">
    <div>
      <div class="text-h1">
        {{ urlCode }}
      </div>

      <div
        class="text-h2"
        style="opacity:.4"
      >
        {{ $t('404') }}
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="primary"
        unelevated
        @click="$router.replace('/')"
        :label="$t('home')"
        no-caps
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
  name: 'Error404',
  setup () {
    const urlCode = <string>(window.location.pathname.split('/').pop())

    return {
      urlCode
    }
  }
})

</script>
