<template>
  <q-page>
    <div class="flex flex-col items-center">
      <div class="max-w-5xl">
        <div>
          <q-btn
            @click="$router.replace('/')"
            rounded
            color="white"
            text-color="primary"
            class="ml-3 mt-9 text-subtitle2 text-weight-bold"
          >
            <span class="material-icons mr-1 mb-.5">
              arrow_back_ios
            </span>
            <div class="mt-0.5">
              {{ $t('home') }}
            </div>
          </q-btn>
          <div class="mt-9 pl-3 text-5xl text-gray-600">
            {{ $t('settings') }}
          </div>
          <hr class="mt-3">
          <div class="flex flex-col">
            <q-list>
              <q-item-label
                header
                class="pr-12 text-2xl"
              >
                {{ $t('components') }}
              </q-item-label>

              <div class="text-base ml-4 mb-4 text-gray-600">
                {{ $t('click_toggle') }}
              </div>
              <q-item
                clickable
                v-ripple
                tag="a"
                target="_self"
                href="/upload-files/"
              >
                <q-icon
                  name="folder"
                  color="orange"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('file_manager') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('files_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-model="files"
                  icon="folder"
                  class="self-end"
                  size="lg"
                  :disable="togglesLoading"
                  v-if="!filesLoading && !wifiLoading"
                  @update:model-value="updateFiles"
                />
                <q-spinner
                  v-if="filesLoading || wifiLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>

              <q-item
                clickable
                v-ripple
                tag="a"
                target="_self"
                :disable="!internet"
                @click="redirect"
              >
                <q-tooltip
                  v-if="!internet"
                  anchor="top middle"
                  self="center middle"
                  :offset="[10, 10]"
                  style="font-size: 16px"
                >
                  {{ $t('need_connection') }}
                </q-tooltip>
                <q-icon
                  name="import_contacts"
                  color="green"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('library') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('library_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-model="library"
                  icon="import_contacts"
                  size="lg"
                  :disable="togglesLoading"
                  v-if="!libraryLoading && !wifiLoading"
                  @update:model-value="updateLibrary"
                />
                <q-spinner
                  v-if="libraryLoading || wifiLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>

              <q-item
                clickable
                v-ripple
                :disable="!internet"
                tag="a"
                target="_self"
                to="/upload_makerspace"
              >
                <q-tooltip
                  v-if="!internet"
                  style="font-size: 16px"
                  anchor="top middle"
                  self="center middle"
                  :offset="[10, 10]"
                >
                  {{ $t('need_connection') }}
                </q-tooltip>
                <q-icon
                  name="create"
                  color="blue"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('makerspace') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('makerspace_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-model="makerspace"
                  icon="create"
                  size="lg"
                  :disable="togglesLoading"
                  v-if="!makerspaceLoading && !wifiLoading"
                  @update:model-value="updateMakerspace"
                />
                <q-spinner
                  v-if="makerspaceLoading || wifiLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>

              <q-item
                clickable
                v-ripple
                tag="a"
                target="_self"
                href="/upload-website/"
              >
                <q-icon
                  name="language"
                  color="yellow"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('website') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('website_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-model="website"
                  icon="language"
                  size="lg"
                  class="ml-auto"
                  :disable="togglesLoading"
                  v-if="!websiteLoading && !wifiLoading"
                  @update:model-value="updateWebsite"
                />
                <q-spinner
                  v-if="websiteLoading || wifiLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>
            </q-list>
            <q-separator spaced />

            <q-item-label
              header
              class="text-2xl"
            >
              {{ $t('login') }}
            </q-item-label>

            <q-btn
              outline
              rounded
              no-caps
              color="primary"
              @click="$router.replace('password_reset')"
              :label="$t('set_password')"
              class="ml-3 mr-3 mb-2 text-lg"
            />

            <q-btn
              outline
              rounded
              no-caps
              color="primary"
              @click="disableLoginWarn"
              :label="$t('disable_password')"
              class="ml-3 mr-3 mb-2 text-lg"
            />

            <q-separator spaced />
            <q-item-label
              header
              class="text-2xl"
            >
              {{ $t('wifi') }}
            </q-item-label>
            <div>
              <div class="text-lg ml-4">
                <div v-if="wifiLoading">
                  {{ $t('status') }}: {{ $t('loading') }}
                </div>
                <div v-else-if="!wifi">
                  {{ $t('status') }}: {{ $t('disconnected') }}
                </div>
                <div v-else>
                  {{ $t('status') }}: {{ $t('connected') }}
                </div>
              </div>
            </div>
            <q-btn
              outline
              rounded
              :loading="wifiLoading"
              no-caps
              v-model="wifi"
              color="primary"
              @click="wifiWarn"
              class="ml-3 mr-3 mt-1 mb-2 text-lg"
              :disable="wifiLoading"
              :label="!wifi ? $t('connect'): $t('disconnect')"
            />
          </div>
          <q-list
            bordered
            class="rounded-borders mt-5 "
          >
            <q-expansion-item
              expand-separator
              icon="build"
              :label="$t('advanced')"
              class="w-full"
            >
              <div class="text-lg ml-6 mt-6">
                {{ $t('set_hostname_desc') }}
              </div>
              <q-card>
                <q-card-section>
                  <q-input
                    ref="hostnameValid"
                    filled
                    class="ml-1 mr-1 text-lowercase"
                    :rules="[(val) =>
                      !val.includes(' ') &&
                      val.length <= 32
                      && val === val.toLowerCase()
                      && regexp.test(val)
                      || $t('invalid_input')]"
                    v-model="newHostname"
                    :label="$t('hostname')"
                  />
                  <q-btn
                    outline
                    rounded
                    no-caps
                    color="primary"
                    @click="hostnameWarn"
                    :label="$t('set_hostname')"
                    class="full-width ml-3 mr-3 mt-6 sm:mt-1 mb-4 text-lg"
                  />
                  <q-separator spaced />

                  <div>
                    <q-item class="flex">
                      <q-item-section>
                        <q-item-label class="josefin text-xl mt-3">
                          {{ $t('portainer') }}
                        </q-item-label>
                        <q-item-label class="text-base pr-1 text-gray-500">
                          {{ $t('portainer_settings_description') }}
                        </q-item-label>
                      </q-item-section>

                      <q-toggle
                        class="mt-3 self-end"
                        v-model="portainer"
                        @update:model-value="updatePortainer"
                        :disable="portainerToggleLoading"
                        v-if="!portainerLoading && !wifiLoading"
                        icon="widgets"
                        size="lg"
                      />
                      <q-spinner
                        v-if="portainerLoading || wifiLoading"
                        color="primary"
                        size="2em"
                        class="mt-6 mr-6"
                      />
                    </q-item>
                  </div>
                  <div
                    class="pl-6"
                    v-if="portainer"
                    href="/test"
                  >
                    {{ $t('portainer_starting_at') }}: <a href="/portainer/">http://{{ windowHostname }}/portainer/</a>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
          <div class="text-center text-2xl mt-6 mb-4 text-gray-600">
            {{ $t('system_info') }}
          </div>
          <div
            v-if="!sysInfoLoading"
            class="flex flex-col text-center text-gray pb-5"
          >
            <span class="text-gray-600"><span>{{ $t('total_storage') }}: </span>{{ sysInfo.storage.total }}</span>
            <span class="text-gray-600"><span>{{ $t('available_storage') }}: </span> {{ sysInfo.storage.available }}</span>
            <span class="text-gray-600"><span>{{ $t('version') }}: </span>{{ sysInfo.versions.lb }}</span>
          </div>
          <div
            v-else
            class="flex flex-col text-center text-gray pb-5"
          >
            <span class="text-gray-600"><span>Loading...</span>{{ sysInfo.versions.lb }}</span>
          </div>
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
import { useI18n } from 'vue-i18n'

export default defineComponent({
  name: 'Settings',
  setup () {
    const $store = useStore()
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()
    const files = ref<boolean>(false)
    const filesLoading = ref<boolean>(false)
    const hostname = ref<string>('')
    const internet = ref<boolean>(false)
    const hostnameValid = ref()
    const library = ref<boolean>(false)
    const libraryLoading = ref<boolean>(false)
    const loading = ref<boolean>(false)
    const makerspace = ref<boolean>(false)
    const makerspaceLoading = ref<boolean>(false)
    const newHostname = ref<string>('')
    const portainer = ref<boolean>(false)
    const portainerLoading = ref<boolean>(false)
    const portainerToggleLoading = ref<boolean>(true)
    // Regular expression for input validation
    // eslint-disable-next-line prefer-regex-literals
    const regexp = ref(new RegExp('^[a-z0-9-_]*$'))
    const sysInfoLoading = ref<boolean>(true)
    const sysInfo = ref<{storage: {total: string, available: string}, versions:{lb: string}}>({ storage: { total: '', available: '' }, versions: { lb: '' } })
    const togglesLoading = ref<boolean>(true)
    const website = ref<boolean>(false)
    const websiteLoading = ref<boolean>(false)
    const wifi = ref<boolean>(false)
    const wifiLoading = ref<boolean>(true)
    const windowHostname = ref<string>(window.location.hostname)

    // Get api from store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // API calls for onMounted
    const fetchedSettings = Axios.get(`${api.value}/v1/settingsui`)
    const fetchedPortainer = Axios.get(`${api.value}/v1/portainer/status`)
    const fetchedSysInfo = Axios.get(`${api.value}/v1/system/info`)
    const fetchedConnectionStatus = Axios.get(`${api.value}/v1/wifi/connectionstatus`)
    const fetchedInternetConnectionStatus = Axios.get(`${api.value}/v1/internet/connectionstatus`)
    const fetchedHostName = Axios.get(`${api.value}/v1/hostname`)

    onMounted(() => {
      apiCall()
    })

    async function apiCall (): Promise<void> {
      await Axios.all([fetchedSettings, fetchedPortainer, fetchedSysInfo,
        fetchedConnectionStatus, fetchedInternetConnectionStatus,
        fetchedHostName]).then(Axios.spread(function (res1, res2, res3, res4, res5, res6): void {
        // Get settings
        files.value = res1.data.files
        website.value = res1.data.website
        library.value = res1.data.library
        makerspace.value = res1.data.makerspace
        togglesLoading.value = false
        // Get portainer status
        portainer.value = res2.data.container_status === 'Running'
        portainerToggleLoading.value = false
        // Get SystemInfo
        sysInfo.value = res3.data
        sysInfoLoading.value = false
        // Get connection status
        wifi.value = res4.data.running !== false
        wifiLoading.value = false
        // Get internet connection status
        internet.value = res5.data.connected !== false
        // Get hostname
        hostname.value = res6.data.hostname
      }))
    }

    const connectDisconnectWifi = async () => {
      await Axios.get(`${api.value}/v1/wifi/forget`)
    }

    const disableLogin = async () => {
      const response = await Axios.post(`${api.value}/v1/setpassword`, { password: ' ' })
      if (response.status === 200) {
        $q.notify({ type: 'positive', message: t('login_disabled') })
      } else {
        $q.notify({ type: 'negative', message: t('error') })
      }
    }

    function disableLoginWarn () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true
      }).onOk(() => {
        disableLogin()
      })
    }

    function hostnameWarn () {
      if (hostnameValid.value.validate() && newHostname.value !== '') {
        $q.dialog({
          title: t('confirm'),
          message: t('change_hostname_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          updateHostname()

          $q.dialog({
            title: t('success'),
            message: t('hostname_changed_notification')
          })
        }).onCancel(() => {
          // console.log('>>>> Cancel')
        }).onDismiss(() => {
          // console.log('I am triggered on both OK and Cancel')
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_hostname') })
      }
    }

    function redirect () {
      location.href = '/upload-library/'
    }

    const updateFiles = async () => {
      filesLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        files: files.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        filesLoading.value = false
      }, 1)
    }

    const updateLibrary = async () => {
      libraryLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        library: library.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        libraryLoading.value = false
      }, 1)
    }

    const updateMakerspace = async () => {
      makerspaceLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        makerspace: makerspace.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        makerspaceLoading.value = false
      }, 1)
    }

    const updatePortainer = async () => {
      portainerLoading.value = true

      if (portainer.value) {
        await Axios.get(`${api.value}/v1/portainer/start`)
      } else {
        await Axios.get(`${api.value}/v1/portainer/stop`)
      }

      setTimeout(() => {
        portainerLoading.value = false
      }, 1)
    }

    const updateWebsite = async () => {
      websiteLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        website: website.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        websiteLoading.value = false
      }, 1)
    }

    const updateHostname = async () => {
      if (newHostname.value) {
        await Axios.post(`${api.value}/v1/hostconfig`, {
          hostname: newHostname.value
        })
      }
    }

    function wifiWarn () {
      if (internet.value && !wifi.value) {
        $q.notify({ type: 'negative', message: t('internet_no_wifi') })
      } else if (wifi.value === false) {
        window.open('http://' + window.location.hostname + `:8080/index.html?lang=${$q.lang.isoName}`)
      } else {
        $q.dialog({
          title: t('confirm'),
          message: t('disconnect_wifi'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          connectDisconnectWifi()
          wifi.value = false
        }).onCancel(() => {
          // console.log('>>>> Cancel')
        })
      }
    }

    return {
      disableLogin,
      disableLoginWarn,
      files,
      filesLoading,
      hostname,
      hostnameValid,
      hostnameWarn,
      internet,
      library,
      libraryLoading,
      loading,
      makerspace,
      makerspaceLoading,
      newHostname,
      portainer,
      portainerLoading,
      portainerToggleLoading,
      redirect,
      regexp,
      sysInfo,
      sysInfoLoading,
      togglesLoading,
      updateFiles,
      updateLibrary,
      updateMakerspace,
      updatePortainer,
      website,
      websiteLoading,
      wifi,
      wifiLoading,
      wifiWarn,
      windowHostname,
      updateWebsite
    }
  }
})
</script>

<style scoped>

</style>
