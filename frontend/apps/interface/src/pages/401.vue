<template>
  <div
    class="fullscreen bg-primary text-white text-center q-pa-md flex flex-center"
  >
    <div>
      <div class="text-h1">401</div>

      <div class="text-h2" style="opacity: 0.4">
        {{ $t('401') }}
      </div>

      <q-btn
        class="q-mt-xl"
        color="white"
        text-color="primary"
        unelevated
        :label="$t('home')"
        no-caps
        @click="$router.replace('/')"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'IntError401'
})
</script>
