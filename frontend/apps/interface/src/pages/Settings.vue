<template>
  <q-page>
    <div class="flex flex-col items-center text-subtitle1">
      <div
        class="q-gutter-y-md items-center window-width"
      >
        <q-tabs
          v-model="tab"
          class="bg-primary text-gray-900"
          shrink
          dense
          inline-label
          outside-arrows
          mobile-arrows
        >
          <q-tab
            name="home"
            icon="home"
            @click="$router.push('/')"
          />
          <q-tab
            name="general"
            icon="build"
            :label="$t('general')"
          />
          <q-tab
            name="appStore"
            icon="storefront"
            :label="$t('app_store')"
          />
          <q-tab
            name="advanced"
            icon="settings"
            :label="$t('advanced')"
          />
        </q-tabs>
      </div>
      <div
        v-if="tab == 'general'"
        class="q-pa-sm"
        style="min-width: 70vw"
      >
        <!-- Component toggles -->
        <q-list padding>
          <q-item-label
            header
          >
            <q-item-section class="text-h6">
              {{ $t('components') }}
            </q-item-section>
            <q-item-section>
              {{ $t('click_toggle') }}
            </q-item-section>
          </q-item-label>
          <!-- File Manager -->
          <q-item
            clickable
            :to="{ name: 'filemanager', params: { data: 'fileshare'} }"
          >
            <q-item-section
              top
              avatar
            >
              <q-avatar
                icon="folder"
                text-color="orange"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>
                {{ $t('file_manager') }}
              </q-item-label>
              <q-item-label caption>
                {{ $t('files_settings_description') }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-toggle
                v-if="!filesLoading"
                v-model="files"
                icon="folder"
                :disable="togglesLoading"
                @update:model-value="updateFiles"
              />
              <q-spinner
                v-if="filesLoading"
                color="primary"
                size="2em"
                class="mt-1 mr-2"
              />
            </q-item-section>
          </q-item>
          <!-- Library -->
          <q-item
            clickable
            tag="a"
            target="_self"
            :disable="!internet || wifiLoading"
            :to="{ name: 'library' }"
          >
            <q-tooltip
              v-if="!internet && !wifiLoading"
              class="text-caption text-center"
              anchor="top middle"
              self="center middle"
              :offset="[10, 10]"
            >
              {{ $t('need_internet_connection') }}
            </q-tooltip>
            <q-item-section
              top
              avatar
            >
              <q-avatar
                icon="import_contacts"
                text-color="green"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>
                {{ $t('library') }}
              </q-item-label>
              <q-item-label caption>
                {{ $t('library_settings_description') }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-btn
                icon="edit"
                outline
                dense
                flat
                size="md"
                color="primary"
                :to="{ name: 'filemanager', params: { data: 'library'} }"
                @click.stop
              >
                <q-tooltip
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[10, 10]"
                >
                  {{ $t('manage_library_files') }}
                </q-tooltip>
              </q-btn>
            </q-item-section>
            <q-item-section side>
              <q-toggle
                v-if="!libraryLoading"
                v-model="library"
                icon="import_contacts"
                :disable="togglesLoading"
                @update:model-value="updateLibrary"
              />
              <q-spinner
                v-if="libraryLoading"
                color="primary"
                size="2em"
                class="mt-1 mr-2"
              />
            </q-item-section>
          </q-item>
          <!-- Website -->
          <q-item
            clickable
            :to="{ name: 'filemanager', params: { data: 'website'} }"
          >
            <q-item-section
              top
              avatar
            >
              <q-avatar
                icon="language"
                text-color="yellow"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>
                {{ $t('website') }}
              </q-item-label>
              <q-item-label caption>
                {{ $t('website_settings_description') }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-toggle
                v-if="!websiteLoading"
                v-model="website"
                icon="language"
                class="ml-auto"
                :disable="togglesLoading"
                @update:model-value="updateWebsite"
              />
              <q-spinner
                v-if="websiteLoading"
                color="primary"
                size="2em"
                class="mt-1 mr-2"
              />
            </q-item-section>
          </q-item>

          <q-separator spaced />
          <!-- Security section -->
          <q-item-label
            header
            class="text-h6"
          >
            {{ $t('security') }}
          </q-item-label>
          <q-card flat>
            <q-item
              clickable
              :disable="settingPassword || togglesLoading"
              @click="setLoginPassword()"
            >
              <q-item-section
                top
                avatar
              >
                <q-avatar
                  v-if="loginPasswordStatus"
                  icon="lock"
                  text-color="green"
                />
                <q-avatar
                  v-else
                  icon="lock_open"
                  text-color="accent"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>
                  {{ $t('set_cp_password') }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t('set_cp_password_desc') }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  v-model="loginPasswordToggle"
                  :icon="loginPasswordToggle ? 'lock' : 'lock_open'"
                  :disable="settingPassword || togglesLoading"
                  @update:model-value="setLoginPassword()"
                />
              </q-item-section>
            </q-item>
            <!-- Wifi Passwords -->
            <q-item
              clickable
              :disable="settingPassword || togglesLoading"
              @click="setWifiPassword()"
            >
              <q-item-section
                top
                avatar
              >
                <q-avatar
                  v-if="wifiPasswordStatus"
                  icon="lock"
                  text-color="green"
                />
                <q-avatar
                  v-else
                  icon="lock_open"
                  text-color="accent"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>
                  {{ $t('set_wifi_password') }}
                </q-item-label>
                <q-item-label caption>
                  {{ $t('set_wifi_password_desc') }}
                </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  v-model="wifiPasswordToggle"
                  :icon="wifiPasswordToggle ? 'lock' : 'lock_open'"
                  :disable="settingPassword || togglesLoading"
                  @update:model-value="setWifiPassword()"
                />
              </q-item-section>
            </q-item>
            <q-inner-loading :showing="settingPassword || togglesLoading">
              <q-spinner-gears
                size="50px"
                color="primary"
              />
            </q-inner-loading>
          </q-card>
          <q-separator spaced />
          <!-- Networking section -->
          <q-item-label
            header
          >
            <q-item-section class="text-h6">
              {{ $t('networking') }}
            </q-item-section>
            <q-item-section>
              {{ $t('connect_wifi_desc') }}
            </q-item-section>
          </q-item-label>
          <q-btn
            v-model="wifi"
            class="ml-3 mr-3 mt-1 mb-2 text-base full-width"
            icon="wifi"
            outline
            rounded
            :loading="wifiLoading"
            no-caps
            color="primary"
            :disable="wifiLoading"
            :label="!wifi ? $t('connect'): $t('disconnect')"
            @click="wifiWarn"
          />
        </q-list>
        <q-separator spaced />
      </div>
      <!-- Application Store -->
      <div
        v-if="tab == 'appStore'"
        class="q-pa-sm"
        style="min-width: 70vw"
      >
        <q-table
          v-if="rows"
          flat
          wrap-cells
          :loading="!appTableVisible"
          :rows="rows"
          :rows-per-page-options="[10, 20, 0]"
          :grid="$q.screen.xs"
          :no-data-label="$t('no_apps_to_display')"
          :no-results-label="$t('no_apps_to_display')"
          :table-class="appTableVisible ? 'text-black': 'text-white'"
          :columns="columns"
          row-key="application"
        >
          <template #loading>
            <q-inner-loading
              showing
              flat
              color="primary"
            >
              <div
                class="flex justify-center"
                style="background-color: white"
              >
                <q-spinner-gears
                  size="50px"
                  color="primary"
                />
                <div class="mt-2 text-center text-base text-gray-800">
                  {{ $t('this_may_take_time') }}
                </div>
              </div>
            </q-inner-loading>
          </template>
          <template #top-left>
            <q-item-label
              header
              class="text-h6"
            >
              {{ $t('available_applications') }}
            </q-item-label>
          </template>
          <template #top-right>
            <q-btn
              round
              size="xs"
              icon="refresh"
              :disable="wifiLoading"
              @click="internet ? refreshApps(): $q.notify({ type: 'negative', message: $t('need_internet_connection') })"
            />
          </template>
          <template
            v-if="appTableVisible"
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
            v-if="appTableVisible"
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
                >
                  <q-badge
                    v-if="props.row.status == 'update_available'"
                    color="accent"
                    floating
                  />
                </q-btn>
              </div>
            </q-td>
          </template>
          <!-- Application Store Mobile templates -->
          <template #item="props">
            <div
              class="pl-3 pr-3 q-pa-xs col-xs-12 col-sm-6 col-md-4"
              :class="appTableVisible ? 'text-black': 'text-white'"
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
                  <strong>{{ props.row.long_name }}</strong>
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
                  <div class="text-gray-600">
                    {{ props.row.info }}
                  </div>
                  <div class="text-gray-600">
                    {{ $t('version') }} {{ props.row.version_name }}
                  </div>
                  <q-btn
                    v-if="appTableVisible"
                    class="mb-1"
                    size="sm"
                    unelevated
                    color="primary"
                    :label="$t(props.row.status)"
                    @click="toggleApp(props.row)"
                  >
                    <q-badge
                      v-if="props.row.status == 'update_available'"
                      color="accent"
                      floating
                    />
                  </q-btn>
                </q-list>
              </q-card>
            </div>
          </template>
        </q-table>
        <q-card
          v-else
          flat
        >
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
      </div>
      <!-- Advanced Features -->
      <div
        v-if="tab == 'advanced'"
        class="mt-1 pd-2"
        style="min-width: 70vw"
      >
        <q-list
          dense
        >
          <q-item-label
            header
          >
            <q-item-section class="text-h6">
              {{ $t('choose_start_page') }}
            </q-item-section>
            <q-item-section>
              {{ $t('start_page_desc') }}
            </q-item-section>
          </q-item-label>
          <q-item class="mb-1">
            <q-select
              v-if="!filesLoading"
              v-model="selectedStartPage"
              class="full-width"
              :loading="!selectedStartPage"
              rounded
              dense
              outlined
              transition-duration="1"
              :options="startPageOptions"
              @update:model-value="changeStartPage"
            />
          </q-item>
          <!-- Custom start page -->
          <q-slide-transition :duration="2000">
            <div v-show="customStartPageInput">
              <q-item
                class="justify-center"
              >
                <q-input
                  ref="startPathValid"
                  v-model="customStartPath"
                  class="mt-1 ml-1 mr-1 fit ml-2 mr-2"
                  filled
                  dense
                  hide-bottom-space
                  :label="$t('choose_new_path')"
                  :placeholder="$t('your_new_path')"
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
                      padding="0"
                      round
                      dense
                      flat
                      color="primary"
                      icon="check_circle_outline"
                      :disable="customStartPath === ''"
                      @click="storeStartPage(null)"
                    />
                  </template>
                </q-input>
              </q-item>
            </div>
          </q-slide-transition>
          <q-separator
            class="mr-3 ml-3 mt-4"
          />
          <!-- Choose App as default path -->
          <q-dialog
            v-model="appStorePageInput"
          >
            <q-card style="width: 700px; max-width: 80vw;">
              <q-card-section class="row items-center">
                <q-table
                  v-if="rows"
                  :title="$t('available_applications')"
                  flat
                  dense
                  wrap-cells
                  separator="cell"
                  style="width: 700px; max-width: 80vw;"
                  :grid="$q.screen.xs"
                  :rows-per-page-options="[0]"
                  :rows="rows"
                  :table-class="appTableVisible ? 'text-black': 'text-white'"
                  :columns="columns"
                  :visible-columns="visibleColumns"
                  filter="installed"
                  row-key="application"
                  :no-data-label="$t('no_apps_installed')"
                  :no-results-label="$t('no_apps_installed')"
                >
                  <template
                    v-if="appTableVisible"
                    #body-cell-status="props"
                  >
                    <q-td :props="props">
                      <div>
                        <q-btn
                          v-close-popup
                          unelevated
                          color="primary"
                          size="sm"
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
                        <q-card-section class="text-center text-body1 text-weight-bold q-pa-none mt-2">
                          {{ props.row.long_name }}
                        </q-card-section>
                        <q-separator />
                        <q-list
                          dense
                          class="text-center"
                        >
                          <q-btn
                            v-close-popup
                            class="mb-2 mt-2"
                            size="sm"
                            rounded
                            unelevated
                            color="secondary"
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
                  @click="selectedStartPage = $t('choose_start_page')"
                />
              </q-card-actions>
            </q-card>
          </q-dialog>
          <!-- Set Hostname/URL/WiFi SSID -->
          <q-item-label
            header
          >
            <q-item-section class="text-h6">
              {{ $t('set_hostname_desc') }}
            </q-item-section>
            <q-item-section>
              {{ $t('url_wifi_desc') }}
            </q-item-section>
          </q-item-label>
          <q-item>
            <q-input
              ref="hostnameValid"
              v-model="newHostname"
              class="ml-1 mr-1 full-width mb-4"
              filled
              dense
              hide-bottom-space
              :label="$t('enter_name')"
              :placeholder="$t('your_new_name')"
              :rules="[(val) =>
                val.length <= 32
                && regexp.test(val)
                || $t('invalid_input')]"
            >
              <template #after>
                <q-btn
                  class="mt-1"
                  padding="0"
                  round
                  dense
                  flat
                  :loading="hostnameChanging"
                  color="primary"
                  icon="check_circle_outline"
                  :disable="newHostname"
                  @click="hostnameWarn"
                />
              </template>
              <template
                v-if="newHostname"
                #hint
              >
                <div class="text-caption text-gray-800">
                  <div>{{ $t('your_new_url') }} <span class="text-primary">'http://{{ newHostname.replaceAll(" ", "").toLowerCase() }}.local'</span></div>
                  <div
                    v-if="newHostname=='lb'"
                  >
                    {{ $t('your_new_ssid') }} <span class="text-primary">'Learner's Block'</span>
                  </div>
                  <div v-else>
                    {{ $t('your_new_ssid') }} <span class="text-primary">'{{ newHostname }}'</span>
                  </div>
                </div>
              </template>
            </q-input>
          </q-item>
          <q-separator
            class="mr-3 ml-3"
          />
          <!-- Portainer -->
          <q-item-label
            header
            class="text-h6"
          >
            {{ $t('portainer') }}
          </q-item-label>
          <q-item class="mb-3">
            <q-tooltip
              v-if="portainerUnavailable && !portainerLoading"
              class="text-caption text-center"
              anchor="top middle"
              self="center middle"
              :offset="[10, 10]"
            >
              {{ $t('need_internet_connection') }}
            </q-tooltip>
            <q-item-section
              top
              avatar
            >
              <q-avatar
                icon="widgets"
                :text-color="portainer ? 'primary' : 'accent'"
              />
            </q-item-section>
            <q-item-section bottom>
              <q-item-label>
                {{ $t('portainer_settings_description') }}
              </q-item-label>
              <q-item-label caption>
                {{ $t('portainer_desc') }}
              </q-item-label>
              <q-item-label
                v-if="portainer && !portainerLoading"
                caption
              >
                {{ $t('portainer_starting_at') }} <a
                  :href="'http://' + windowHostname + ':9000'"
                  target="_blank"
                >http://{{ windowHostname }}:9000</a>
              </q-item-label>
              <q-item-label
                v-if="portainer && portainerLoading && !portainerImageExists"
                caption
              >
                {{ $t('portainer_installing') }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-toggle
                v-if="!portainerLoading"
                v-model="portainer"
                :disable="portainerLoading || portainerUnavailable"
                icon="widgets"
                @update:model-value="updatePortainer"
              />
              <q-spinner
                v-if="portainerLoading"
                color="primary"
                size="2em"
              />
            </q-item-section>
          </q-item>
          <q-separator
            class="mr-3 ml-3"
            spaced
          />
          <!-- System Maintenance -->
          <q-expansion-item>
            <template #header>
              <q-item-section class="text-h6 text-gray-500">
                {{ $t('system_maintenance') }}
              </q-item-section>
              <q-item-section side>
                <div class="row items-center">
                  <q-icon
                    color="accent"
                    name="warning"
                  />
                </div>
              </q-item-section>
            </template>
            <q-card>
              <!-- Prune System Files -->
              <q-item>
                <q-item-section
                  top
                  avatar
                >
                  <q-avatar
                    icon="delete"
                    text-color="red"
                  />
                </q-item-section>
                <q-item-section bottom>
                  <q-item-label>
                    {{ $t('prune_system_files_description') }}
                  </q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-btn
                    outline
                    rounded
                    no-caps
                    :loading="systemMaintenance"
                    size="md"
                    color="red"
                    :label="$t('prune')"
                    class="text-lg"
                    @click="pruneSystemFiles"
                  />
                </q-item-section>
              </q-item>
              <!-- Reset Database -->
              <q-item>
                <q-item-section
                  top
                  avatar
                >
                  <q-avatar
                    icon="restart_alt"
                    text-color="red"
                  />
                </q-item-section>
                <q-item-section bottom>
                  <q-item-label>
                    {{ $t('reset_database_description') }}
                  </q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-btn
                    outline
                    rounded
                    no-caps
                    :loading="systemMaintenance"
                    size="md"
                    color="red"
                    :label="$t('reset')"
                    class="text-lg"
                    @click="resetDatabase"
                  />
                </q-item-section>
              </q-item>
            </q-card>
          </q-expansion-item>
        </q-list>
        <q-separator spaced />
        <!-- System Info -->
        <div class="text-center text-xl mt-4 text-gray-600">
          {{ $t('system_info') }}
        </div>
        <div
          v-if="!sysInfoLoading"
          class="flex flex-col text-center text-gray pb-5 items-center text-caption text-gray-600"
        >
          <div>
            {{ $t('total_storage') }} {{ sysInfo.storage.total }}
          </div>
          <div>
            {{ $t('available_storage') }} {{ sysInfo.storage.available }}
          </div>
          <div>
            {{ $t('version') }} {{ sysInfo.versions.lb }}
          </div>
          <div
            v-if="!wifiLoading"
            class="row"
          >
            <q-icon
              v-if="devMode"
              class="mr-1"
              color="primary"
              name="developer_mode"
              size="xs"
            />
            <q-icon
              v-if="internet && !wifi"
              class="mr-1"
              color="primary"
              name="cable"
              size="xs"
            />
            <q-icon
              class="mr-1"
              :color="wifi ? 'primary' : 'accent'"
              :name="wifi ? 'wifi' : 'wifi_off'"
              size="xs"
            />
            <q-icon
              :color="internet ? 'primary' : 'accent'"
              :name="internet ? 'public' : 'public_off'"
              size="xs"
            />
          </div>
        </div>
        <div
          v-else
          class="flex flex-col text-center text-gray pb-5"
        >
          <div class="text-gray-600">
            Loading...
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import Axios from 'axios'
import { AxiosOverride } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const $store = useStore()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    const appStorePageInput = ref<boolean>(false)
    const appTableVisible = ref(false)
    const customStartPageInput = ref<boolean>(false)
    const customStartPath = ref<any>('')
    const devMode = ref<boolean>(false)
    const files = ref<boolean>(false)
    const filesLoading = ref<boolean>(true)
    const hostnameChanging = ref<boolean>(false)
    const hostnameValid = ref()
    const internet = ref<boolean>(false)
    const lang = computed(() => {
      return ref($q.lang.isoName)
    })
    const library = ref<boolean>(false)
    const libraryLoading = ref<boolean>(true)
    const loginPasswordStatus = ref<boolean>(false)
    const loginPasswordToggle = ref<boolean>(false)
    const newHostname = ref<any>('')
    const portainer = ref<boolean>(false)
    const portainerImageExists = ref<boolean>(true)
    const portainerLoading = ref<boolean>(true)
    const portainerUnavailable = ref<boolean>(true)
    // Regular expression for input validation
    // eslint-disable-next-line prefer-regex-literals
    const regexp = ref(new RegExp('^[A-Za-z0-9-_]'))
    const $router = useRouter()
    const settingPassword = ref<boolean>(false)
    const selectedStartPage = ref<any>('')
    const startPathValid = ref()
    const sysInfoLoading = ref<boolean>(true)
    const sysInfo = ref<{storage: {total: string, available: string}, versions:{lb: string}}>({ storage: { total: '', available: '' }, versions: { lb: '' } })
    const systemMaintenance = ref<boolean>(false)
    const togglesLoading = ref<boolean>(true)
    const website = ref<boolean>(false)
    const websiteLoading = ref<boolean>(true)
    const wifi = ref<boolean>(false)
    const wifiPasswordStatus = ref<boolean>(false)
    const wifiPasswordToggle = ref<boolean>(false)
    const wifiLoading = ref<boolean>(true)
    const windowHostname = ref<string>(window.location.hostname)

    // Get api from store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // App Store database
    const columns = computed(() => [
      {
        name: 'name',
        required: true,
        label: t('application'),
        align: 'left',
        field: row => row.long_name,
        format: val => `${val}`,
        sortable: true
      },
      { name: 'author_site', label: t('author'), field: 'author_site', align: 'left', sortable: true },
      { name: 'info', label: t('info'), field: 'info', align: 'left' },
      { name: 'version', label: t('version'), field: 'version_name', align: 'left' },
      { name: 'ports', field: 'ports' },
      { name: 'status', field: 'status', sortable: true, align: 'center' }
    ]) as any

    const rows = ref<any>(null)

    const startPageOptions = computed(() => [
      {
        label: t('lb_welcome_page'),
        string: '/'
      },
      {
        label: t('file_manager'),
        string: 'files'
      },
      {
        label: t('library'),
        string: 'library'
      },
      {
        label: t('website'),
        string: 'website'
      },
      {
        label: t('custom_start_page'),
        string: selectedStartPage.value ? selectedStartPage.value.string : ''
      },
      {
        label: t('app_store_app'),
        string: rows.value ? rows.value.find(x => x.name === selectedStartPage.value) : ''
      }
    ])

    watch(lang, () => {
      selectedStartPage.value = t('choose_start_page')
    })

    onMounted(() => {
      apiCall()
    })

    // Populate variables on first load of page
    function apiCall () {
      // API calls for Axios spread
      const fetchedConnectionStatus = Axios.get(`${api.value}/v1/wifi/connection_status`)
      const fetchedPortainerSettings = Axios.post(`${api.value}/v1/system/portainer`, { cmd: 'status' })
      const settingsUi = Axios.get(`${api.value}/v1/settings/get_ui`)
      const verifyUserPasswordState = Axios.get(`${api.value}/v1/auth/verify_user_password_state`)

      // Group dependent calls together for Portainer and Connection Status
      Promise.all([fetchedConnectionStatus, fetchedPortainerSettings]).then(function ([res1, res2]) {
        // Set connection status
        if (res1.data.wifi) {
          wifi.value = true
        }

        // Set internet connection status
        if (res1.data.internet) {
          internet.value = true
        } else {
          internet.value = false
        }

        // Set Portainer status. Dependent on having fetched internet connection status.
        if (res2.data.installed) {
          portainer.value = true
          portainerUnavailable.value = false
        } else if (!res2.data.image && !internet.value) {
          portainer.value = false
          portainerImageExists.value = res2.data.image
          portainerUnavailable.value = true
        } else {
          portainer.value = false
          portainerImageExists.value = res2.data.image
          portainerUnavailable.value = false
        }

        portainerLoading.value = false
        wifiLoading.value = false
      })

      // Fetch Settings UI configuration
      Promise.all([settingsUi, verifyUserPasswordState]).then(async function ([res1, res2]) {
        // Set settings toggle status
        files.value = res1.data.files
        website.value = res1.data.website
        library.value = res1.data.library
        devMode.value = res1.data.dev_mode

        // Check if disable wifi password button should be visible
        if (res1.data.wifi_password_set) {
          wifiPasswordStatus.value = true
          wifiPasswordToggle.value = true
        }

        // Check if disable password button should be visible
        if (res2.data.default_login_password_set) {
          loginPasswordStatus.value = true
          loginPasswordToggle.value = true
        }

        // Stop loading toggles
        togglesLoading.value = false
        filesLoading.value = false
        libraryLoading.value = false
        websiteLoading.value = false

        // Fetch available apps from database.
        await fetchApps()

        // Set default start page
        const internalPage = startPageOptions.value.find((x) => x.string === res1.data.start_page)?.label
        const appEntry = rows.value.find(x => x.name === res1.data?.start_page)
        if (internalPage) {
          selectedStartPage.value = internalPage
        } else if (appEntry) {
          selectedStartPage.value = appEntry.long_name
        } else {
          selectedStartPage.value = res1.data.start_page
        }
      })

      // Fetch System Info status
      Axios.get(`${api.value}/v1/system/info`).then((response) => {
        sysInfo.value = response.data
        sysInfoLoading.value = false
      })
    }

    // Show various dialogs or execute functions depending on user selection
    const changeStartPage = () => {
      if (selectedStartPage.value.label === t('app_store_app')) {
        customStartPageInput.value = false
        appStorePageInput.value = true
      } else if (selectedStartPage.value.label === t('custom_start_page')) {
        appStorePageInput.value = false
        customStartPageInput.value = true
      } else {
        storeStartPage(null)
      }
    }

    // Function for calling delays throughout
    function delay (ms: number) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }

    // Forget current Wi-Fi connection
    const disconnectWifi = async () => {
      await Axios.get(`${api.value}/v1/wifi/forget`)
    }

    // Fetch a list of apps as stored in the local database. Does not query the online database
    async function fetchApps () {
      appTableVisible.value = false
      await Axios.get(`${api.value}/v1/appstore/status`).then((availableApps) => {
        rows.value = availableApps.data
        appTableVisible.value = true
      }
      )
    }

    // Verify that the user wants to change the hostname
    function hostnameWarn () {
      if (hostnameValid.value.validate() && newHostname.value !== '') {
        $q.dialog({
          title: t('confirm'),
          message: t('change_hostname_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          updateHostname()
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_hostname') })
      }
    }

    // Notify that the hostname has been changed
    function permNotify (type, message) {
      $q.notify({
        type: type,
        message: message,
        timeout: 0,
        actions: [
          {
            label: t('close'),
            color: 'white',
            handler: () => { /* ... */ }
          }
        ]
      })
    }

    // Remove unused system files such as Docker images
    function pruneSystemFiles () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true,
        dark: true
      }).onOk(() => {
        systemMaintenance.value = true
        Axios.get(`${api.value}/v1/system/prune`).then(() => {
          portainerImageExists.value = false
          // Only return False on success, as redirect will take care of boolean otherwise
          systemMaintenance.value = false
          $q.notify({ type: 'positive', message: t('success') })
        })
      })
    }

    // A simple redirect to another page
    function redirect (path) {
      location.href = path
    }

    // Fetch list of new apps from the online database and update local databse
    async function refreshApps () {
      appTableVisible.value = false
      await Axios.get(`${api.value}/v1/appstore/get_apps`)
      await Axios.get(`${api.value}/v1/appstore/status`).then((availableApps) => {
        rows.value = availableApps.data
      }
      )
      appTableVisible.value = true
    }

    // Reset the SQLite database
    function resetDatabase () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true,
        dark: true
      }).onOk(() => {
        systemMaintenance.value = true
        $q.loading.show()
        AxiosOverride.get(`${api.value}/v1/system/reset_database`, { timeout: 1000 }).catch(function () {
          resetDatabaseLoop()
        })
      })
    }

    // Check for when the API is back up after the SQLite database reset, and when ready forward
    // user back to first page
    async function resetDatabaseLoop () {
      const redirecting = ref<boolean>(false)
      for (let i = 0; i < 10; i++) {
        await delay(4000)
        const xhr = new XMLHttpRequest()
        xhr.open('GET', api.value)
        xhr.timeout = 2000

        xhr.onreadystatechange = async function () {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 0 || (xhr.status >= 200 && xhr.status < 400)) {
              redirecting.value = true
              await delay(7000)
              redirect('/')
            }
          }
        }

        if (!redirecting.value) {
          xhr.send()
        } else {
          return
        }
      }
      $q.notify({ type: 'negative', message: t('api_down') })
    }

    // Change the password used to access the Control Panel (also known as the settings panel)
    function setLoginPassword () {
      if (loginPasswordStatus.value) {
        $q.dialog({
          title: t('disable_password'),
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(async () => {
          settingPassword.value = true
          await Axios.post(`${api.value}/v1/auth/set_password`, { password: ' ' }).then(() => {
            $q.notify({ type: 'positive', message: t('login_disabled') })
            loginPasswordStatus.value = false
            loginPasswordToggle.value = false
          })
          settingPassword.value = false
        }).onCancel(() => {
          loginPasswordToggle.value = true
        })
      } else {
        $q.dialog({
          title: t('set_password'),
          cancel: true,
          persistent: true,
          prompt: {
            model: '',
            type: 'password'
          }
        }).onOk(async (data) => {
          settingPassword.value = true
          await Axios.post(`${api.value}/v1/auth/set_password`, {
            password: data
          }).then(() => {
            $q.notify({ type: 'positive', message: t('password_set_success') })
            loginPasswordStatus.value = true
            loginPasswordToggle.value = true
          })
          settingPassword.value = false
        }).onCancel(() => {
          loginPasswordToggle.value = false
        })
      }
    }

    // Set a password for accessing the Wi-Fi
    function setWifiPassword () {
      if (wifiPasswordStatus.value) {
        $q.dialog({
          title: t('disable_password'),
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(async () => {
          settingPassword.value = true
          await Axios.post(`${api.value}/v1/wifi/set_password`, { wifi_password: '' }).then(() => {
            $q.notify({ type: 'positive', message: t('wifi_login_disabled') })
            wifiPasswordStatus.value = false
            wifiPasswordToggle.value = false
          })
          settingPassword.value = false
        }).onCancel(() => {
          wifiPasswordToggle.value = true
        })
      } else {
        $q.dialog({
          title: t('set_password'),
          message: t('invalid_wifi_entry'),
          cancel: true,
          persistent: true,
          prompt: {
            model: '',
            isValid: val => val.length > 7,
            type: 'password'
          }
        }).onOk(async (data) => {
          settingPassword.value = true
          await Axios.post(`${api.value}/v1/wifi/set_password`, {
            wifi_password: data
          }).then(() => {
            $q.notify({ type: 'positive', message: t('wifi_password_set_success') })
            wifiPasswordStatus.value = true
            wifiPasswordToggle.value = true
          })
          settingPassword.value = false
        }).onCancel(() => {
          wifiPasswordToggle.value = false
        })
      }
    }

    // Commit the passed start page to the database
    async function storeStartPage (rows) {
      // If reseting to default, do not prompt user for confirmation
      if (selectedStartPage.value.label === t('lb_welcome_page')) {
        await Axios.post(`${api.value}/v1/settings/set_ui`, {
          start_page: '/'
        })
        $q.notify({ type: 'positive', message: `${t('path_changed_to')} ${selectedStartPage.value.label}` })
      } else if (rows || (customStartPath.value && customStartPageInput)) {
        $q.dialog({
          title: t('confirm'),
          message: `${t('change_path_warning')} http://${windowHostname.value}/settings`,
          cancel: true,
          persistent: true
        }).onOk(() => {
          // If an app store app is passed to this function
          if (rows) {
            Axios.post(`${api.value}/v1/settings/set_ui`, {
              start_page: rows.name
            })
            $q.notify({ type: 'positive', message: `${t('path_changed_to')} ${rows.long_name}` })
            // If a custom path name
          } else if (customStartPath.value && customStartPageInput) {
            if (startPathValid.value.validate()) {
              Axios.post(`${api.value}/v1/settings/set_ui`, {
                start_page: customStartPath.value
              })
              $q.notify({ type: 'positive', message: `${t('path_changed_to')} '${customStartPath.value}'` })
              customStartPath.value = ''
            } else {
              $q.notify({ type: 'negative', message: t('invalid_path_input') })
            }
          }
        })
      } else {
        Axios.post(`${api.value}/v1/settings/set_ui`, {
          start_page: selectedStartPage.value.string
        })
        $q.notify({ type: 'positive', message: `${t('path_changed_to')} ${selectedStartPage.value.label}` })
      }
    }

    // Toggle through the various states for the passed application (install, installed, update etc.)
    async function toggleApp (row) {
      if (row.status.toLowerCase() === 'install') {
        // If the internet is not available, cannot pull images
        if (!internet.value) {
          // If the image already exists, it can still install
          const imageExists = await AxiosOverride.post(`${api.value}/v1/docker/image`, {
            image: row.image
          }).then(function (res) {
            if (res.data.image) {
              return true
            } else {
              return false
            }
          }).catch(function () {
            return false
          })

          // If the image doesn't exist, exit the function and notify the user
          if (!imageExists) {
            $q.notify({ type: 'negative', message: t('need_internet_connection') })
            return
          }
        }

        // Prompt user to confirm install
        $q.dialog({
          title: `${t('install')} ${row.long_name}`,
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(async () => {
          appTableVisible.value = false
          // Install app
          await Axios.post(`${api.value}/v1/docker/run`, {
            env_vars: row.env_vars,
            image: row.image,
            name: row.name,
            ports: row.ports,
            volumes: row.volumes,
            dependencies: row.dependencies
          }).then(function () {
            permNotify('positive', t('app_installed'))
            fetchApps()
          }).catch(async function () {
            await fetchApps()
          })
          appTableVisible.value = true
        })
      } else if (row.status.toLowerCase() === 'installed') {
        $q.dialog({
          title: `${t('uninstall')} ${row.long_name}`,
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(async () => {
          appTableVisible.value = false
          // Uninstall app
          await Axios.post(`${api.value}/v1/docker/remove`, {
            name: row.name,
            dependencies: row.dependencies
          }).then(function () {
            $q.notify({ type: 'positive', message: t('success') })
            fetchApps()
          }).catch(async function () {
            await fetchApps()
          })
          appTableVisible.value = true
        })
      } else if (row.status.toLowerCase() === 'update_available') {
        if (!internet.value) {
          $q.notify({ type: 'negative', message: t('need_internet_connection') })
          return
        }
        $q.dialog({
          title: `${t('update')} ${row.long_name}`,
          message: t('are_you_sure'),
          cancel: true,
          persistent: true
        }).onOk(async () => {
          appTableVisible.value = false
          // Update app
          await Axios.post(`${api.value}/v1/docker/pull`, {
            env_vars: row.env_vars,
            image: row.image,
            name: row.name,
            ports: row.ports,
            volumes: row.volumes,
            dependencies: row.dependencies
          }).then(function () {
            permNotify('positive', t('app_installed'))
            fetchApps()
          }).catch(async function () {
            await fetchApps()
          })
          appTableVisible.value = true
        })
      }
    }

    // Update files toggle
    const updateFiles = async () => {
      filesLoading.value = true
      await Axios.post(`${api.value}/v1/settings/set_ui`, {
        files: !!files.value
      })
      filesLoading.value = false
    }

    // Update the Wi-Fi SSID and Hostname
    const updateHostname = async () => {
      if (newHostname.value) {
        hostnameChanging.value = true
        $q.loading.show()

        // Change the Wi-Fi SSID first otherwise the container is killed by the hostname
        // change before it can recieve the request.

        // Set new Wi-Fi SSID
        await Axios.post(`${api.value}/v1/wifi/set_ssid`, {
          ssid: newHostname.value
        }).then(async function () {
          // If the Wi-Fi SSID change is successful, request change for hostname.
          // Use the AxiosOverride as it is going to timeout when connected via the Wi-Fi hotspot.
          await AxiosOverride.post(`${api.value}/v1/supervisor/host_config`, {
            hostname: newHostname.value,
            timeout: 4000
          }).then(async function () {
            await delay(10000)
            permNotify('positive', t('hostname_changed_notification'))
          }).catch(async function (error) {
            // Return positive message if there was no response. A timout
            // is expected as the device is connecting to a new network.
            if (!error.response) {
              // Add delay before returning response to ensure hostname has had time to apply
              await delay(10000)
              permNotify('positive', t('hostname_changed_notification'))
            } else {
              permNotify('negative', t('error'))
              console.log(error)
            }
          })
        })
        hostnameChanging.value = false
        $q.loading.hide()
      }
    }

    // Update library toggle
    const updateLibrary = async () => {
      libraryLoading.value = true
      await Axios.post(`${api.value}/v1/settings/set_ui`, {
        library: !!library.value
      })
      libraryLoading.value = false
    }

    // Toggle between Portainer being enabled or disabled
    const updatePortainer = async () => {
      portainerLoading.value = true
      if (portainer.value) {
        await Axios.post(`${api.value}/v1/system/portainer`, { cmd: 'start' }).then(function () {
          portainerImageExists.value = true
        }).catch(function () {
          // Set the toggle back to its starting position
          portainer.value = false
          // Ensure loading indicators are disabled to allow further use of UI
          portainerLoading.value = false
        })
      } else {
        await Axios.post(`${api.value}/v1/system/portainer`, { cmd: 'remove' }).catch(function () {
          // Set the toggle back to its starting position
          portainer.value = true
          // Ensure loading indicators are disabled to allow further use of UI
          portainerLoading.value = false
        })
      }
      portainerLoading.value = false
    }

    // Update website toggle
    const updateWebsite = async () => {
      websiteLoading.value = true
      await Axios.post(`${api.value}/v1/settings/set_ui`, {
        website: !!website.value
      })
      websiteLoading.value = false
    }

    // Warn before setting a password for the Wi-Fi hotspot
    function wifiWarn () {
      if (wifi.value === false) {
        $router.push('/wifi')
      } else {
        $q.dialog({
          title: t('confirm'),
          message: t('disconnect_wifi'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          wifiLoading.value = true
          disconnectWifi()
          // Add delay to improve user interaction
          setTimeout(() => {
            wifi.value = false
            wifiLoading.value = false
          }, 2000)
        })
      }
    }

    return {
      appStorePageInput,
      appTableVisible,
      changeStartPage,
      columns,
      customStartPageInput,
      customStartPath,
      devMode,
      files,
      filesLoading,
      hostnameChanging,
      hostnameValid,
      hostnameWarn,
      internet,
      library,
      libraryLoading,
      loginPasswordStatus,
      loginPasswordToggle,
      newHostname,
      portainer,
      portainerImageExists,
      portainerLoading,
      portainerUnavailable,
      pruneSystemFiles,
      refreshApps,
      regexp,
      resetDatabase,
      rows,
      setLoginPassword,
      setWifiPassword,
      settingPassword,
      systemMaintenance,
      selectedStartPage,
      startPageOptions,
      startPathValid,
      storeStartPage,
      sysInfo,
      sysInfoLoading,
      tab: ref('general'),
      toggleApp,
      togglesLoading,
      updateFiles,
      updateLibrary,
      updatePortainer,
      updateWebsite,
      visibleColumns: ref(['author_site', 'status']),
      website,
      websiteLoading,
      wifi,
      wifiLoading,
      wifiPasswordStatus,
      wifiPasswordToggle,
      wifiWarn,
      windowHostname
    }
  }
})
</script>

<style scoped>

</style>
