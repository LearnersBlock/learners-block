<template>
  <q-page>
    <div class="flex flex-col items-center">
      <div class="max-w-5xl">
        <div class="mt-10 text-4xl text-gray-600 mb-6 text-center">
          {{ $t('welcome') }}
        </div>
        <q-separator />
        <q-list v-if="!allIsDisabled">
          <q-item
            v-if="settings.files"
            class="cursor-pointer py-3"
            tag="a"
            target="_self"
            href="/files"
          >
            <q-item-section
              side
              middle
            >
              <q-icon
                name="folder"
                color="orange"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label class="josefin text-2xl pr-12">
                {{ $t('files') }}
              </q-item-label>
              <q-item-label class="text-lg text-gray-500">
                {{ $t('files_description') }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.files" />

          <q-item
            v-if="settings.library"
            class="cursor-pointer py-3"
            tag="a"
            target="_blank"
            href="https://library.learnersblock.org"
          >
            <q-item-section
              side
              middle
            >
              <q-icon
                name="import_contacts"
                color="green"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label class="josefin text-2xl pr-12">
                {{ $t('library') }}
              </q-item-label>
              <q-item-label class="text-lg text-gray-500">
                {{ $t('library_description') }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.library" />

          <q-item
            v-if="settings.makerspace"
            class="cursor-pointer py-3"
            to="/makerspace"
            target="_self"
          >
            <q-item-section
              side
              middle
            >
              <q-icon
                name="create"
                color="blue"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label class="josefin text-2xl pr-12">
                {{ $t('makerspace') }}
              </q-item-label>
              <q-item-label class="text-lg text-gray-500">
                {{ $t('makerspace_description') }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.makerspace" />

          <q-item
            v-if="settings.website"
            class="cursor-pointer py-3"
            tag="a"
            target="_self"
            href="/website"
          >
            <q-item-section
              side
              middle
            >
              <q-icon
                name="language"
                color="yellow"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label class="josefin text-2xl pr-12">
                {{ $t('website') }}
              </q-item-label>
              <q-item-label class="text-lg text-gray-500">
                {{ $t('website_description') }}
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator v-if="settings.website" />
        </q-list>
        <div
          v-if="!settings.website && !settings.files && !settings.makerspace && !settings.library"
          class="text-2xl text-gray-500 mt-3 text-center ml-1 mr-1"
        >
          {{ $t('enable_components_in') }}
        </div>
      </div>
    </div>
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