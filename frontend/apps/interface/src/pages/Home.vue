<template>
  <q-page>
    <div class="flex flex-col items-center">
      <div class="max-w-5xl">
        <div class="mt-10 text-4xl text-gray-600 mb-6 text-center ml-2 mr-2">
          {{ $t('welcome_lb') }}
        </div>
        <q-separator />
        <q-list v-if="!allIsDisabled">
          <q-item
            v-if="settings.files"
            class="cursor-pointer py-3"
            tag="a"
            target="_self"
            href="/files/"
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
            target="_self"
            href="/library/"
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
            v-if="settings.website"
            class="cursor-pointer py-3"
            tag="a"
            target="_self"
            href="/website/"
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
        <div v-if="slides[0]">
          <q-item-label
            header
            class="text-2xl"
          >
            {{ $t('app_store') }}
          </q-item-label>

          <div class="q-pl-md q-pr-md q-pb-md">
            <div class="q-gutter-md">
              <q-carousel
                transition-prev="scale"
                transition-next="scale"
                swipeable
                animated
                control-color="primary"
                navigation
                padding
                arrows
                height="200px"
                class="text-plsrimary text-2xl shadow-1 rounded-borders"
                v-model="slide"
              >
                <q-carousel-slide
                  v-for="slide in slides"
                  :key="slide.name"
                  :name="slide.name"
                  class="column no-wrap flex-center cursor-pointer"
                  @click="redirect('http://' + windowHostname + ':' + slide.ports)"
                >
                  <q-icon
                    name="apps"
                    size="56px"
                    color="primary"
                  />
                  <div class="q-mt-md text-center">
                    {{ slide.long_name }}
                  </div>
                </q-carousel-slide>
              </q-carousel>
            </div>
          </div>
        </div>

        <div
          v-if="settingsLoading"
          class="text-2xl text-gray-500 mt-3 text-center ml-1 mr-1"
        >
          {{ $t('loading') }}
        </div>
        <div
          v-else-if="!settings.website && !settings.files && !settings.library"
          class="text-2xl text-gray-500 mt-3 text-center ml-1 mr-1"
        >
          {{ $t('enable_components_in') }}
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import Axios from 'app/node_modules/axios'
import { useQuasar } from 'quasar'
import { useStore } from '../store'

export default defineComponent({
  setup () {
    // Import required features
    const $store = useStore()
    const $q = useQuasar()

    // App Store
    const jsonKey = ref<any>()
    const slide = ref<any>()
    const slides = ref<any>({})
    const windowHostname = ref<string>(window.location.hostname)

    // Settings for the ui
    const settings = ref<any>({})
    const settingsLoading = ref<boolean>(true)
    // Check to see if everything is disabled
    const allIsDisabled = !!(settings.value.files === false &&
                          settings.value.library === false &&
                          settings.value.website === false)
    // Get API from Store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // Get settings
    onMounted((): void => {
      $q.loading.show({
        delay: 300 // ms
      })

      Axios.get(`${api.value}/v1/settingsui`).then(res => {
        if (res.data.start_page === '/') {
          settings.value = res.data
          settingsLoading.value = false
        } else if (res.data.start_page.substring(0, 1) === ':') {
          setTimeout(() => {
            location.href = `http://${window.location.hostname}${res.data.start_page}`
          }, 2000)
        } else {
          slides.value = Axios.get(`${api.value}/v1/appstore/status`).then((availableApps) => {
            for (let i = 0; i < availableApps.data.length; i++) {
              if (availableApps.data[i].name === res.data.start_page) {
                setTimeout(() => {
                  const appPort = Object.keys(availableApps.data[i].ports)
                  location.href = `http://${window.location.hostname}:${appPort}`
                }, 2000)
                return
              }
              setTimeout(() => {
                location.href = `/${res.data.start_page}/`
              }, 2000)
            }
          }
          )
        }
      }).catch(e => {
        console.log(e.message)
      })

      Axios.get(`${api.value}/v1/appstore/status`).then((availableApps) => {
        let entry = 0
        for (let i = 0; i < availableApps.data.length; i++) {
          if (availableApps.data[i].status.toLowerCase() === 'installed') {
            slides.value[entry] = availableApps.data[i]
            jsonKey.value = Object.keys(availableApps.data[i].ports)
            slides.value[entry].ports = slides.value[entry].ports[jsonKey.value]

            entry = entry + 1
          }
        }
        if (slides.value[0]) {
          slide.value = slides.value[0].name
        }
      }
      )
      $q.loading.hide()
    })

    function redirect (path) {
      location.href = path
    }

    return {
      allIsDisabled,
      redirect,
      settings,
      settingsLoading,
      slide,
      slides,
      windowHostname
    }
  }
})
</script>

<style scoped>

</style>
