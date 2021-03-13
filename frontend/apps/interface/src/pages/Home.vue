<template>
     <q-page class="py-28 px-52">
       <div class="text-5xl text-gray-600">{{ $t('welcome') }}</div>
        <hr class="mt-6 mb-10" />
        <q-list class="w-2/3" bordered v-if="!allIsDisabled">
          <q-item  v-if="settings.files" class="cursor-pointer py-3" tag="a" target="_self" href="https://www.facebook.com">
              <q-item-section>
              <q-item-label class="josefin text-xl">{{$t('files')}}</q-item-label>
              <q-item-label caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
            </q-item-section>

            <q-item-section side middle>
              <q-icon name="folder" color="orange" />
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.files"  />

          <q-item v-if="settings.website"  class="cursor-pointer py-3" tag="a" target="_self" href="https://www.facebook.com">
            <q-item-section>
              <q-item-label class="josefin text-xl">{{ $t('website') }}</q-item-label>
              <q-item-label caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
            </q-item-section>

            <q-item-section side middle>
              <q-icon name="language" color="yellow" />
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.website"  />

          <q-item v-if="settings.makerspace" class="cursor-pointer py-3" to="/makerspace" target="_self" href="https://www.facebook.com">
            <q-item-section>
              <q-item-label class="josefin text-xl">{{ $t('makerspace') }}</q-item-label>
              <q-item-label caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
            </q-item-section>

            <q-item-section side middle>
              <q-icon name="space_bar" color="blue" />
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.makerspace" />

          <q-item v-if="settings.library" to="/library"  class="cursor-pointer py-3" href="https://www.facebook.com">
            <q-item-section>
              <q-item-label class="josefin text-xl">{{ $t('library') }}</q-item-label>
              <q-item-label caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
            </q-item-section>

            <q-item-section side middle>
              <q-icon name="import_contacts" color="green" />
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.library" />

       </q-list>
       <h1 class="text-3xl text-gray-700" v-else>{{ $t('no_url_is_enabled') }}</h1>
     </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from '@vue/composition-api'
import Axios from 'app/node_modules/axios'

export default defineComponent({
  setup (_, { root }) {
    // Settings for the ui
    const settings = ref<any>({})
    // Check to see if everything is disabled
    const allIsDisabled = !!(settings.value.files === false &&
                          settings.value.library === false &&
                          settings.value.website === false &&
                          settings.value.makerspace === false)
    // Get API from Store
    const api = computed(() => {
      return root.$store.getters.GET_API
    })

    // Get settings
    onMounted(async () => {
      Axios.get(`${api.value}/v1/settingsui`).then(res => {
        settings.value = res.data
      }).catch(e => {
        console.log(e.message)
      })
    })

    return {
      settings,
      allIsDisabled
    }
  }
})
</script>

<style scoped>

</style>
