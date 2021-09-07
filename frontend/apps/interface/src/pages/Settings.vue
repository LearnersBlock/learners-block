<template>
  <q-page>
    <div class="flex flex-col items-center">
      <div class="max-w-5xl">
        <div>
          <!-- Home Button -->
          <q-btn
            rounded
            color="white"
            size="sm"
            text-color="primary"
            class="ml-3 mt-7 text-subtitle2 text-weight-bold"
            outline
            :label="$t('home')"
            icon="arrow_back"
            @click="$router.push('/')"
          />
          <!-- Settings label -->
          <div class="mt-8 pl-3 text-5xl text-gray-600">
            {{ $t('settings') }}
          </div>
          <hr class="mt-3">
          <!-- Component toggles -->
          <div class="flex flex-col">
            <q-list>
              <q-item-label
                header
                class="pr-12 text-2xl"
              >
                {{ $t('components') }}
              </q-item-label>
              <!-- File Manager -->
              <div class="text-base ml-4 mb-4 text-gray-600">
                {{ $t('click_toggle') }}
              </div>
              <q-item
                v-ripple
                clickable
                to="/filemanager"
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
                  v-if="!filesLoading"
                  v-model="files"
                  icon="folder"
                  class="self-end"
                  size="lg"
                  :disable="togglesLoading"
                  @update:model-value="updateFiles"
                />
                <q-spinner
                  v-if="filesLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>
              <!-- Library -->
              <q-item
                v-ripple
                clickable
                tag="a"
                target="_self"
                :disable="!internet"
                @click="redirect('/upload-library/')"
              >
                <q-tooltip
                  v-if="!internet"
                  anchor="top middle"
                  self="center middle"
                  :offset="[10, 10]"
                  class="text-caption text-center"
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
                  v-if="!libraryLoading"
                  v-model="library"
                  icon="import_contacts"
                  size="lg"
                  :disable="togglesLoading"
                  @update:model-value="updateLibrary"
                />
                <q-spinner
                  v-if="libraryLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>
              <!-- Website -->
              <q-item
                v-ripple
                clickable
                :to="{ name: 'filemanager', params: { data: 'website'} }"
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
                  v-if="!websiteLoading"
                  v-model="website"
                  icon="language"
                  size="lg"
                  class="ml-auto"
                  :disable="togglesLoading"
                  @update:model-value="updateWebsite"
                />
                <q-spinner
                  v-if="websiteLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>
            </q-list>
            <q-separator spaced />
            <!-- Login section -->
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
              :label="$t('set_password')"
              class="ml-3 mr-3 mb-2 text-lg"
              @click="$router.push('password_reset')"
            />
            <q-btn
              v-if="showPasswordButton"
              outline
              :loading="togglesLoading"
              rounded
              no-caps
              color="primary"
              :label="$t('disable_password')"
              class="ml-3 mr-3 mb-2 text-lg"
              @click="disableLoginWarn"
            />
            <q-separator spaced />
            <!-- Wi-Fi section -->
            <q-item-label
              header
              class="text-2xl"
            >
              {{ $t('wifi') }}
            </q-item-label>
            <div>
              <div class="text-lg ml-4">
                <div v-if="wifiLoading">
                  {{ $t('status') }} {{ $t('loading') }}
                </div>
                <div v-else-if="!wifi">
                  {{ $t('status') }} {{ $t('disconnected') }}
                </div>
                <div v-else>
                  {{ $t('status') }} {{ $t('connected') }}
                </div>
              </div>
            </div>
            <q-btn
              v-model="wifi"
              outline
              rounded
              :loading="wifiLoading"
              no-caps
              color="primary"
              class="ml-3 mr-3 mt-1 mb-2 text-lg"
              :disable="wifiLoading"
              :label="!wifi ? $t('connect'): $t('disconnect')"
              @click="wifiWarn"
            />
            <q-btn
              outline
              rounded
              no-caps
              color="primary"
              :loading="settingWifiPassword || togglesLoading"
              :label="$t('set_password')"
              class="ml-3 mr-3 mb-2 text-lg"
              @click="setWifiPasswordDialog = true"
            />
            <q-dialog
              v-model="setWifiPasswordDialog"
              persistent
            >
              <q-card style="width: 700px; max-width: 80vw;">
                <q-card-section class="row items-center">
                  <q-input
                    ref="wifiPasswordValid"
                    v-model="wifiPassword"
                    class="ml-1 mr-1"
                    style="width: 700px; max-width: 80vw;"
                    filled
                    type="password"
                    :placeholder="$t('password')"
                    :rules="[(value) =>
                      !value.includes(' ') &&
                      value.length > 7
                      || $t('invalid_wifi_entry')]"
                  />
                </q-card-section>
                <q-card-actions align="right">
                  <q-btn
                    v-close-popup
                    flat
                    :label="$t('cancel')"
                    color="primary"
                    @click="wifiPassword = ''"
                  />
                  <q-btn
                    v-close-popup
                    flat
                    :label="$t('set_password')"
                    color="primary"
                    @click="wifiPasswordChange"
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>
            <q-btn
              v-if="showWifiPasswordButton"
              outline
              :loading="settingWifiPassword || togglesLoading"
              rounded
              no-caps
              color="primary"
              :label="$t('disable_password')"
              class="ml-3 mr-3 mb-2 text-lg"
              @click="disableWifiWarn"
            />
          </div>
          <!-- Application Store -->
          <q-list
            bordered
            class="rounded-borders mt-2"
          >
            <q-expansion-item
              expand-separator
              icon="storefront"
              :label="$t('app_store')"
              class="w-full"
            >
              <q-table
                v-if="rows"
                :title="$t('available_applications')"
                flat
                bordered
                :loading="appTableVisible"
                :grid="$q.screen.xs"
                :rows-per-page-options="[3, 5, 10]"
                :rows="rows"
                :table-class="!appTableVisible ? 'text-black': 'text-white'"
                :columns="columns"
                row-key="application"
                :no-data-label="$t('no_apps_to_display')"
              >
                <template #loading>
                  <q-inner-loading
                    showing
                    color="primary"
                  >
                    <q-spinner-gears
                      size="50px"
                      color="primary"
                    />
                    <div class="mt-1 text-base text-center text-gray-800">
                      {{ $t('this_may_take_time') }}
                    </div>
                  </q-inner-loading>
                </template>
                <template #top-right>
                  <q-btn
                    round
                    size="xs"
                    icon="refresh"
                    @click="internet ? refreshApps(): $q.notify({ type: 'negative', message: $t('need_connection') })"
                  />
                </template>
                <template
                  v-if="!appTableVisible"
                  #body-cell-author_site="props"
                >
                  <q-td :props="props">
                    <div>
                      <a
                        :href="'http://'+ props.row.author_site"
                        target="_blank"
                      >{{ props.row.author_site }}</a>
                    </div>
                  </q-td>
                </template>
                <template
                  v-if="!appTableVisible"
                  #body-cell-status="props"
                >
                  <q-td :props="props">
                    <div>
                      <q-btn
                        size="xs"
                        unelevated
                        color="primary"
                        :label="$t(props.value)"
                        @click="toggleApp(props.row)"
                      />
                    </div>
                  </q-td>
                </template>

                <!-- Application Store Mobile templates -->
                <template #item="props">
                  <div
                    class="pl-3 pr-3 q-pa-xs col-xs-12 col-sm-6 col-md-4"
                    :class="!appTableVisible ? 'text-black': 'text-white'"
                  >
                    <q-card>
                      <q-card-section class="text-center">
                        <q-img
                          v-if="props.row.logo"
                          :src="props.row.logo"
                          style="max-width: 56px"
                        />
                        <q-icon
                          v-else
                          name="apps"
                          size="56px"
                          color="primary"
                        />
                        <br>
                        <strong>{{ props.row.name }}</strong>
                      </q-card-section>
                      <q-separator />
                      <q-list
                        dense
                        class="text-center"
                      >
                        <div>
                          {{ $t('author_colon') }} <a
                            :href="'http://'+ props.row.author_site"
                            target="_blank"
                          >{{ props.row.author_site }}</a>
                        </div>

                        <div>{{ $t('version') }} {{ props.row.version }}</div>
                        <q-btn
                          v-if="!appTableVisible"
                          class="mb-1"
                          size="xs"
                          unelevated
                          color="primary"
                          :label="$t(props.row.status)"
                          @click="toggleApp(props.row)"
                        />
                      </q-list>
                    </q-card>
                  </div>
                </template>
              </q-table>
              <q-card v-else>
                <q-card-section>
                  <div class="column flex text-base text-center items-center text-gray-800">
                    <q-spinner-gears
                      size="50px"
                      color="primary"
                    />
                    {{ $t('this_may_take_time') }}
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
          <!-- Advanced Features -->
          <q-list
            bordered
            class="rounded-borders mt-4"
          >
            <q-expansion-item
              expand-separator
              icon="build"
              :label="$t('advanced')"
              class="w-full"
            >
              <q-card>
                <q-card-section>
                  <div class="mr-3 ml-3">
                    <div class="text-2xl text-gray-700">
                      {{ $t('choose_start_page') }}
                    </div>
                    <div class="text-base text-gray-500 mb-1">
                      {{ $t('start_page_desc') }}
                    </div>
                    <q-select
                      v-if="!filesLoading"
                      v-model="startPage"
                      rounded
                      outlined
                      transition-duration="1"
                      :options="pages"
                      class="mb-5"
                      @update:model-value="changeStartPage"
                    />
                    <div
                      v-if="customStartPageInput"
                      class="text-lg"
                    >
                      {{ $t('choose_new_path') }}
                    </div>
                    <!-- Choose App as default path -->
                    <q-dialog
                      v-model="appStorePageInput"
                      persistent
                    >
                      <q-card style="width: 700px; max-width: 80vw;">
                        <q-card-section class="row items-center">
                          <q-table
                            v-if="rows"
                            :title="$t('available_applications')"
                            flat
                            separator="cell"
                            style="width: 700px; max-width: 80vw;"
                            :grid="$q.screen.xs"
                            :rows-per-page-options="[5, 10]"
                            :rows="rows"
                            :table-class="!appTableVisible ? 'text-black': 'text-white'"
                            :columns="columns"
                            :visible-columns="visibleColumns"
                            filter="installed"
                            row-key="application"
                            :no-data-label="$t('no_apps_to_display')"
                          >
                            <template
                              v-if="!appTableVisible"
                              #body-cell-status="props"
                            >
                              <q-td :props="props">
                                <div>
                                  <q-btn
                                    v-close-popup
                                    size="xs"
                                    unelevated
                                    color="primary"
                                    :label="$t('set_custom_startpage')"
                                    @click="storeStartPage(props.row)"
                                  />
                                </div>
                              </q-td>
                            </template>
                            <!-- Mobile templates -->
                            <template #item="props">
                              <div class="pl-3 pr-3 q-pa-xs col-xs-12 col-sm-6 col-md-4">
                                <q-card>
                                  <q-card-section class="text-center">
                                    <strong>{{ props.row.name }}</strong>
                                  </q-card-section>
                                  <q-separator />
                                  <q-list
                                    dense
                                    class="text-center"
                                  >
                                    <div>
                                      {{ $t('author_colon') }} {{ props.row.author_site }}
                                    </div>
                                    <q-btn
                                      v-close-popup
                                      class="mb-1"
                                      size="xs"
                                      unelevated
                                      color="primary"
                                      :label="$t('set_custom_startpage')"
                                      @click="storeStartPage(props.row)"
                                    />
                                  </q-list>
                                </q-card>
                              </div>
                            </template>
                          </q-table>
                        </q-card-section>
                        <q-card-actions align="right">
                          <q-btn
                            v-close-popup
                            flat
                            :label="$t('cancel')"
                            color="primary"
                            @click="setStartPage"
                          />
                        </q-card-actions>
                      </q-card>
                    </q-dialog>
                    <!-- Custom start page -->
                    <q-slide-transition :duration="2000">
                      <div v-show="customStartPageInput">
                        <q-input
                          v-if="customStartPageInput"
                          ref="startPathValid"
                          v-model="newStartPath"
                          filled
                          :placeholder="$t('your_new_path')"
                          class="ml-1 mr-1"
                          :rules="[(value) =>
                            !value.substr(0,1).includes('/') &&
                            !value.substr(-1).includes('/') &&
                            !value.includes(' ') &&
                            !value.includes('\\')
                            || $t('invalid_path_input')]"
                        >
                          <template #after>
                            <q-btn
                              class="mt-1"
                              round
                              dense
                              flat
                              color="primary"
                              icon="check_circle_outline"
                              @click="newStartPathWarn"
                            />
                          </template>
                        </q-input>
                      </div>
                    </q-slide-transition>
                    <q-separator spaced />
                    <!-- Set Hostname -->
                    <div class="text-2xl text-gray-700 mt-5 mb-1">
                      {{ $t('set_hostname_desc') }}
                    </div>
                    <q-input
                      ref="hostnameValid"
                      v-model="newHostname"
                      filled
                      class="ml-1 mr-1"
                      :rules="[(val) =>
                        !val.includes(' ') &&
                        val.length <= 32
                        && val === val.toLowerCase()
                        && regexp.test(val)
                        || $t('invalid_input')]"
                      :placeholder="$t('your_new_name')"
                    >
                      <template #after>
                        <q-btn
                          class="mt-1"
                          round
                          dense
                          flat
                          color="primary"
                          icon="check_circle_outline"
                          :disable="newHostname"
                          @click="hostnameWarn"
                        />
                      </template>
                    </q-input>
                  </div>
                  <q-separator
                    class="mr-3 ml-3"
                    spaced
                  />
                  <!-- Portainer -->
                  <div>
                    <q-item class="flex">
                      <q-item-section>
                        <q-item-label class="text-2xl text-gray-700">
                          {{ $t('portainer') }}
                        </q-item-label>
                        <q-item-label class="text-base pr-1 text-gray-500">
                          {{ $t('portainer_settings_description') }}
                        </q-item-label>
                      </q-item-section>
                      <q-toggle
                        v-if="!portainerLoading"
                        v-model="portainer"
                        class="mt-3 self-end"
                        :disable="portainerLoading"
                        icon="widgets"
                        size="lg"
                        @update:model-value="updatePortainer"
                      />
                      <q-spinner
                        v-if="portainerLoading"
                        color="primary"
                        size="2em"
                        class="mt-4 mr-6"
                      />
                    </q-item>
                  </div>
                  <div
                    v-if="portainer && !portainerLoading"
                    class="pl-6"
                  >
                    {{ $t('portainer_starting_at') }} <a
                      href="/portainer/"
                      target="_blank"
                    >http://{{ windowHostname }}/portainer/</a>
                  </div>
                  <q-separator
                    class="mr-3 ml-3"
                    spaced
                  />
                  <!-- Prune System Files -->
                  <div>
                    <q-item class="flex">
                      <q-item-section>
                        <q-item-label class="text-2xl text-gray-700">
                          {{ $t('prune_system_files') }}
                        </q-item-label>
                        <q-item-label class="text-base pr-1 text-gray-500">
                          {{ $t('prune_system_files_description') }}
                        </q-item-label>
                      </q-item-section>
                      <q-btn
                        outline
                        rounded
                        no-caps
                        :loading="pruningFiles"
                        :size="'md'"
                        color="red"
                        :label="$t('prune')"
                        class="text-lg mt-2"
                        @click="pruneSystemFiles"
                      />
                    </q-item>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
          <!-- System Info -->
          <div class="text-center text-2xl mt-6 mb-4 text-gray-600">
            {{ $t('system_info') }}
          </div>
          <div
            v-if="!sysInfoLoading"
            class="flex flex-col text-center text-gray pb-5"
          >
            <span class="text-gray-600"><span>{{ $t('total_storage') }} </span> {{ sysInfo.storage.total }}</span>
            <span class="text-gray-600"><span>{{ $t('available_storage') }} </span> {{ sysInfo.storage.available }}</span>
            <span class="text-gray-600"><span>{{ $t('version') }} </span> {{ sysInfo.versions.lb }}</span>
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
import Axios from 'app/node_modules/axios'
import { useQuasar } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'Settings',
  setup () {
    // Import required features
    const $q = useQuasar()
    const $store = useStore()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    const appStorePageInput = ref<boolean>(false)
    const currentStartPage = ref<any>()
    const customStartPageInput = ref<boolean>(false)
    const files = ref<boolean>(false)
    const filesLoading = ref<boolean>(false)
    const hostname = ref<string>('')
    const hostnameValid = ref()
    const internet = ref<boolean>(false)
    const lang = computed(() => {
      return ref($q.lang.isoName)
    })
    const library = ref<boolean>(false)
    const libraryLoading = ref<boolean>(false)
    const loading = ref<boolean>(false)
    const newHostname = ref<string>('')
    const newStartPath = ref<string>('')
    const pagesString = [
      t('lb_welcome_page'), t('file_manager'), t('library'), t('website'), t('app_store_app'), t('custom_start_page')
    ]
    const pages = ref(pagesString)
    const portainer = ref<boolean>(false)
    const portainerLoading = ref<boolean>(true)
    const pruningFiles = ref<boolean>(false)
    // Regular expression for input validation
    // eslint-disable-next-line prefer-regex-literals
    const regexp = ref(new RegExp('^[a-z0-9-_]*$'))
    const $router = useRouter()
    const settingWifiPassword = ref<boolean>(false)
    const setWifiPasswordDialog = ref<boolean>(false)
    const showPasswordButton = ref<boolean>(false)
    const showWifiPasswordButton = ref<boolean>(false)
    const startPage = ref<string>('-')
    const startPathValid = ref()
    const sysInfoLoading = ref<boolean>(true)
    const sysInfo = ref<{storage: {total: string, available: string}, versions:{lb: string}}>({ storage: { total: '', available: '' }, versions: { lb: '' } })
    const togglesLoading = ref<boolean>(true)
    const appTableVisible = ref(false)
    const website = ref<boolean>(false)
    const websiteLoading = ref<boolean>(false)
    const wifi = ref<boolean>(false)
    const wifiPassword = ref<string>('')
    const wifiPasswordValid = ref()
    const wifiLoading = ref<boolean>(true)
    const windowHostname = ref<string>(window.location.hostname)

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    watch(lang, _val => {
      pages.value = [
        t('lb_welcome_page'), t('file_manager'), t('library'), t('website'), t('app_store_app'), t('custom_start_page')
      ]
      // Prevent repeat of page setting before rows are populated on first load
      if (rows.value) {
        setStartPage()
      }
    })

    // Get api from store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // App Store database
    const columns = [
      {
        name: 'name',
        required: true,
        label: t('application'),
        align: 'left',
        field: row => row.long_name,
        format: val => `${val}`,
        sortable: true
      },
      { name: 'author_site', label: t('author'), field: 'author_site', sortable: true },
      { name: 'version', label: t('version'), field: 'version', sortable: true },
      { name: 'ports', field: 'ports', sortable: true },
      { name: 'status', field: 'status', sortable: true }
    ]

    const rows = ref<any>(null)

    // API calls for Axios Spread
    const fetchedHostName = Axios.get(`${api.value}/v1/hostname`)
    const fetchedInternetConnectionStatus = Axios.get(`${api.value}/v1/internet/connectionstatus`)
    const fetchedSettings = Axios.get(`${api.value}/v1/settingsui`)

    onMounted(() => {
      apiCall()
      apiCallAwait()
    })

    function apiCall () {
      Axios.get(`${api.value}/v1/wifi/connectionstatus`).then((response) => {
        // Set connection status
        if (response.data.running) {
          wifi.value = true
        }

        wifiLoading.value = false
      }).catch(e => {
        console.log(e.message)
      })

      // Set Portainer status
      Axios.post(`${api.value}/v1/container/status`, { container_name: 'portainer' }).then((response) => {
        if (response.data.container_status) {
          portainer.value = true
        }
        portainerLoading.value = false
      }).catch(e => {
        console.log(e.message)
      })

      // Set SysInfo status
      Axios.get(`${api.value}/v1/system/info`).then((response) => {
        sysInfo.value = response.data
        sysInfoLoading.value = false
      }).catch(e => {
        console.log(e.message)
      })
    }

    async function apiCallAwait () {
      filesLoading.value = true
      libraryLoading.value = true
      websiteLoading.value = true
      await Axios.all([fetchedSettings, fetchedInternetConnectionStatus,
        fetchedHostName]).then(Axios.spread(function (res1, res2, res3) {
        // Set settings toggle status
        currentStartPage.value = res1.data.start_page
        files.value = res1.data.files
        website.value = res1.data.website
        library.value = res1.data.library

        // Check if disable password button should be appTableVisible
        if (!res1.data.default_login_password_set) {
          showPasswordButton.value = true
        }

        // Check if disable wifi password button should be appTableVisible
        if (res1.data.wifi_password_set) {
          showWifiPasswordButton.value = true
        }

        // Set internet connection status
        if (res2.data.connected) {
          internet.value = true
          refreshApps()
        } else {
          internet.value = false
          fetchApps()
        }

        // Set hostname
        hostname.value = res3.data.hostname

        // Stop loading toggles
        togglesLoading.value = false
      })).catch(e => {
        console.log(e.message)
      })

      setStartPage()

      filesLoading.value = false
      libraryLoading.value = false
      websiteLoading.value = false
    }

    const changeStartPage = () => {
      if (startPage.value === t('lb_welcome_page') || startPage.value === t('file_manager') || startPage.value === t('library') || startPage.value === t('website')) {
        customStartPageInput.value = false
        appStorePageInput.value = false
      } else if (startPage.value === t('app_store_app')) {
        customStartPageInput.value = false
        appStorePageInput.value = true
        return
      } else if (startPage.value === t('custom_start_page')) {
        appStorePageInput.value = false
        customStartPageInput.value = true
        return
      }
      storeStartPage(null)
    }

    const connectDisconnectWifi = async () => {
      await Axios.get(`${api.value}/v1/wifi/forget`)
    }

    function disableLoginWarn () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true
      }).onOk(() => {
        Axios.post(`${api.value}/v1/setpassword`, { password: ' ' }).then((response) => {
          if (response.status === 200) {
            $q.notify({ type: 'positive', message: t('login_disabled') })
          } else {
            $q.notify({ type: 'negative', message: t('error') })
          }
          showPasswordButton.value = false
        })
      })
    }

    function disableWifiWarn () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true
      }).onOk(() => {
        settingWifiPassword.value = true
        Axios.post(`${api.value}/v1/setwifi`, { wifi_password: '' }).then((response) => {
          if (response.status === 200) {
            $q.notify({ type: 'positive', message: t('login_disabled') })
          } else {
            $q.notify({ type: 'negative', message: t('error') })
          }
          settingWifiPassword.value = false
          showWifiPasswordButton.value = false
        })
      })
    }

    async function fetchApps () {
      appTableVisible.value = true
      await Axios.get(`${api.value}/v1/appstore/status`).then((availableApps) => {
        rows.value = availableApps.data
        appTableVisible.value = false
      }
      )
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

          $q.notify({ type: 'positive', message: t('hostname_changed_notification') })
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_hostname') })
      }
    }

    function newStartPathWarn () {
      if (startPathValid.value.validate() && newStartPath.value !== '') {
        $q.dialog({
          title: t('confirm'),
          message: t('change_path_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          Axios.post(`${api.value}/v1/setui`, {
            start_page: newStartPath.value
          })
          $q.notify({ type: 'positive', message: `${t('path_changed_to')} '${newStartPath.value}'` })
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_path_input') })
      }
    }

    function pruneSystemFiles () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true,
        dark: true
      }).onOk(() => {
        pruningFiles.value = true
        Axios.get(`${api.value}/v1/system/prune`).then(() => {
          pruningFiles.value = false
          $q.notify({ type: 'positive', message: t('success') })
        })
      })
    }

    function redirect (path) {
      location.href = path
    }

    async function refreshApps () {
      appTableVisible.value = true
      await Axios.get(`${api.value}/v1/appstore/set`)
      Axios.get(`${api.value}/v1/appstore/status`).then((availableApps) => {
        rows.value = availableApps.data
        setTimeout(() => {
          appTableVisible.value = false
        }, 500)
      }
      )
    }

    function setStartPage () {
      if (currentStartPage.value === '/') {
        startPage.value = t('lb_welcome_page')
      } else if (currentStartPage.value === 'files') {
        startPage.value = t('file_manager')
      } else if (currentStartPage.value === 'library') {
        startPage.value = t('library')
      } else if (currentStartPage.value === 'website') {
        startPage.value = t('website')
      } else {
        startPage.value = currentStartPage.value

        for (let i = 0; i < rows.value.length; i++) {
          if (rows.value[i].name === currentStartPage.value) {
            startPage.value = rows.value[i].long_name
          }
        }
      }
    }

    async function storeStartPage (rows) {
      if (startPage.value === t('lb_welcome_page')) {
        await Axios.post(`${api.value}/v1/setui`, {
          start_page: '/'
        })
        currentStartPage.value = '/'
        $q.notify({ type: 'positive', message: `${t('path_changed_to')} ${startPage.value}` })
      } else {
        $q.dialog({
          title: t('confirm'),
          message: t('change_path_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          if (rows) {
            Axios.post(`${api.value}/v1/setui`, {
              start_page: rows.name
            })
            currentStartPage.value = rows.name
            $q.notify({ type: 'positive', message: `${t('path_changed_to')} ${rows.long_name}` })
          } else {
            if (startPage.value === t('file_manager')) {
              currentStartPage.value = 'files'
            } else if (startPage.value === t('library')) {
              currentStartPage.value = 'library'
            } else if (startPage.value === t('website')) {
              currentStartPage.value = 'website'
            }

            Axios.post(`${api.value}/v1/setui`, {
              start_page: currentStartPage.value
            })
            $q.notify({ type: 'positive', message: `${t('path_changed_to')} ${startPage.value}` })
          }
          setStartPage()
        }).onDismiss(() => {
          startPage.value = currentStartPage.value
          setStartPage()
        })
      }
    }

    function toggleApp (row) {
      if (row.status.toLowerCase() === 'install') {
        if (!internet.value) {
          $q.notify({ type: 'negative', message: t('need_connection') })
          return
        }
        $q.dialog({
          title: `${t('install')} ${row.long_name}`,
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          appTableVisible.value = true
          // Install app
          Axios.post(`${api.value}/v1/docker/run`, {
            env_vars: row.env_vars,
            image: row.image,
            name: row.name,
            ports: row.ports,
            volumes: row.volumes,
            dependencies: row.dependencies
          }).then(function (response) {
            if (response.status === 200) {
              $q.notify({ type: 'positive', message: t('success') })
            } else {
              $q.notify({ type: 'negative', message: t('error') })
            }
            fetchApps()
            appTableVisible.value = false
          }).catch(function (error) {
            if (error.response) {
              console.log(error.response.data)
              $q.notify({ type: 'negative', message: t('error') })
            }
            fetchApps()
            appTableVisible.value = false
          })
        })
      } else if (row.status.toLowerCase() === 'installed') {
        $q.dialog({
          title: `${t('uninstall')} ${row.long_name}`,
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          appTableVisible.value = true
          // Uninstall app
          Axios.post(`${api.value}/v1/docker/remove`, {
            name: row.name,
            dependencies: row.dependencies
          }).then(function (response) {
            if (response.status === 200) {
              $q.notify({ type: 'positive', message: t('success') })
            } else {
              $q.notify({ type: 'negative', message: t('error') })
            }
            fetchApps()
            appTableVisible.value = false
          }).catch(function (error) {
            if (error.response) {
              console.log(error.response.data)
              $q.notify({ type: 'negative', message: t('error') })
            }
            fetchApps()
            appTableVisible.value = false
          })
        })
      } else if (row.status.toLowerCase() === 'update_available') {
        if (!internet.value) {
          $q.notify({ type: 'negative', message: t('need_connection') })
          return
        }
        $q.dialog({
          title: `${t('update')} ${row.long_name}`,
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          appTableVisible.value = true
          // Update app
          Axios.post(`${api.value}/v1/docker/pull`, {
            env_vars: row.env_vars,
            image: row.image,
            name: row.name,
            ports: row.ports,
            volumes: row.volumes,
            dependencies: row.dependencies
          }).then(function (response) {
            if (response.status === 200) {
              $q.notify({ type: 'positive', message: t('success') })
            } else {
              $q.notify({ type: 'negative', message: t('error') })
            }
            fetchApps()
            appTableVisible.value = false
          }).catch(function (error) {
            if (error.response) {
              console.log(error.response.data)
              $q.notify({ type: 'negative', message: t('error') })
            }
            fetchApps()
            appTableVisible.value = false
          })
        })
      }
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

    const updateHostname = async () => {
      if (newHostname.value) {
        await Axios.post(`${api.value}/v1/hostconfig`, {
          hostname: newHostname.value
        })
      }
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

    const updatePortainer = async () => {
      portainerLoading.value = true
      if (portainer.value) {
        const portainerStarter = await Axios.post(`${api.value}/v1/container/start`, { container_name: 'portainer' })
        if (portainerStarter.status === 404) {
          $q.notify({ type: 'negative', message: t('portainer_unavailable') })
          portainer.value = false
        }
      } else {
        await Axios.post(`${api.value}/v1/container/stop`, { container_name: 'portainer' })
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

    function wifiPasswordChange () {
      if (wifiPasswordValid.value.validate() && wifiPassword.value !== '') {
        $q.dialog({
          title: t('confirm'),
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          settingWifiPassword.value = true
          Axios.post(`${api.value}/v1/setwifi`, {
            wifi_password: wifiPassword.value
          }).then((response) => {
            if (response.status === 200) {
              $q.notify({ type: 'positive', message: t('password_set_success') })
              settingWifiPassword.value = false
            }
          })
          wifiPassword.value = ''
          showWifiPasswordButton.value = true
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_entry') })
        wifiPassword.value = ''
      }
    }

    function wifiWarn () {
      if (internet.value && !wifi.value && !process.env.DEV) {
        $q.notify({ type: 'negative', message: t('internet_no_wifi') })
      } else if (wifi.value === false) {
        $router.push('/wifi')
      } else {
        $q.dialog({
          title: t('confirm'),
          message: t('disconnect_wifi'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          connectDisconnectWifi()
          wifi.value = false
        })
      }
    }

    return {
      appStorePageInput,
      changeStartPage,
      columns,
      customStartPageInput,
      disableLoginWarn,
      disableWifiWarn,
      files,
      filesLoading,
      hostname,
      hostnameValid,
      hostnameWarn,
      internet,
      library,
      libraryLoading,
      loading,
      newHostname,
      newStartPath,
      newStartPathWarn,
      pages,
      portainer,
      portainerLoading,
      pruningFiles,
      pruneSystemFiles,
      redirect,
      refreshApps,
      regexp,
      rows,
      setStartPage,
      settingWifiPassword,
      setWifiPasswordDialog,
      showPasswordButton,
      showWifiPasswordButton,
      startPage,
      startPathValid,
      storeStartPage,
      sysInfo,
      sysInfoLoading,
      toggleApp,
      togglesLoading,
      updateFiles,
      updateLibrary,
      updatePortainer,
      updateWebsite,
      appTableVisible,
      visibleColumns: ref(['author_site', 'status']),
      website,
      websiteLoading,
      wifi,
      wifiLoading,
      wifiPassword,
      wifiPasswordChange,
      wifiPasswordValid,
      wifiWarn,
      windowHostname
    }
  }
})
</script>

<style scoped>

</style>
