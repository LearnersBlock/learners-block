<template>
  <q-page class="items-center p-3 text-body1">
    <!-- Home Button -->
    <q-btn
      @click="$router.back()"
      rounded
      size="sm"
      color="white"
      text-color="primary"
      class="mt-1 mb-2 text-body-1 text-weight-bold"
      outline
      :label="$t('back')"
      icon="arrow_back"
    />
    <q-table
      v-if="rows"
      table-style="width: 90vw;"
      flat
      :dense="!$q.platform.is.mobile"
      wrap-cells
      :loading="loading"
      :rows="rows"
      :rows-per-page-options="[20, 50, 100]"
      :columns="columns"
      :no-data-label="$t('empty_folder')"
      :no-results-label="$t('empty_folder')"
      row-key="name"
      :selection="loginState && !$q.platform.is.mobile ? 'multiple' : 'none'"
      v-model:selected="selected"
      :filter="filter"
      :visible-columns="visibleColumns"
      @row-click="onRowClick"
    >
      <!-- Toolbar -->
      <template #top="props">
        <div class="full-width row reverse-wrap justify-between items-center">
          <div class="mt-1">
            <q-breadcrumbs v-if="!objPath[0]">
              <q-breadcrumbs-el
                class="cursor-pointer"
                icon="home"
              />
            </q-breadcrumbs>
            <q-breadcrumbs v-else>
              <q-breadcrumbs-el
                class="cursor-pointer"
                icon="home"
                color="gray-800"
                @click="objPath.splice(0,objPath.length), updateRows()"
              />
              <q-breadcrumbs-el
                class="cursor-pointer"
                v-for="path in objPath"
                :key="path.value"
                :label="path"
                @click="objPath.length = objPath.indexOf(path) +1, updateRows()"
              />
            </q-breadcrumbs>
          </div>
          <div
            class="mb-2"
            style="margin-left: auto"
          >
            <div>
              <q-btn
                v-if="loginState && safeRoute"
                class="mr-2"
                icon="create_new_folder"
                color="gray-800"
                outline
                rounded
                size="sm"
                @click="newFolderPrompt"
              >
                <q-tooltip
                  class="text-caption text-center text-body1"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('new_folder') }}
                </q-tooltip>
              </q-btn>
              <q-btn
                v-if="loginState && safeRoute && !$q.platform.is.mobile"
                class="mr-2"
                icon="drive_file_move_rtl"
                color="gray-800"
                outline
                rounded
                size="sm"
                :disable="!JSON.parse(JSON.stringify(selected))[0]"
                @click="openFileSelector(JSON.parse(JSON.stringify(selected)))"
              >
                <q-tooltip
                  class="text-caption text-center text-body1"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('move_copy') }}
                </q-tooltip>
              </q-btn>
              <q-btn
                v-if="loginState && safeRoute"
                class="mr-2"
                icon="upload"
                color="gray-800"
                outline
                rounded
                size="sm"
                @click="uploaderDialog = true"
              >
                <q-tooltip
                  class="text-caption text-center text-body1"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('upload') }}
                </q-tooltip>
              </q-btn>
              <q-dialog
                v-model="uploaderDialog"
              >
                <q-uploader
                  style="max-width: 300px"
                  :label="$t('upload')"
                  multiple
                  flat
                  square
                  no-thumbnails
                  with-credentials
                  :filter="checkCharacters"
                  :url="api + '/v1/filemanager/upload'"
                  :headers="[{name: 'rootPath', value: rootPath}, {name: 'savePath', value: JSON.stringify(objPath)}, {name: 'Authorization', value: loginToken}]"
                  @uploaded="updateRows()"
                  @failed="uploadFailed"
                  @rejected="onUploaderRejected"
                  @added="checkUploadOverwrite"
                />
              </q-dialog>
              <q-btn
                v-if="loginState && safeRoute && !$q.platform.is.mobile"
                class="mr-2"
                size="sm"
                color="gray-800"
                rounded
                outline
                icon="delete"
                @click="deleteFile(JSON.parse(JSON.stringify(selected)))"
              >
                <q-tooltip
                  class="text-caption text-center text-body1"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('delete') }}
                </q-tooltip>
              </q-btn>
              <q-btn
                icon="search"
                color="gray-800"
                outline
                rounded
                size="sm"
                @click="searchTable = true"
              >
                <q-tooltip
                  class="text-caption text-center text-body1"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('filter') }}
                </q-tooltip>
              </q-btn>
              <q-input
                v-if="searchTable"
                class="ml-3"
                dense
                debounce="300"
                hide-bottom-space
                v-model="filter"
                :placeholder="$t('filter')"
              />
              <q-btn
                v-if="!$q.platform.is.mobile"
                flat
                round
                dense
                :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
                @click="props.toggleFullscreen"
                class="q-ml-md"
              >
                <q-tooltip
                  class="text-caption text-center text-body1"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('full_screen') }}
                </q-tooltip>
              </q-btn>
            </div>
          </div>
        </div>
      </template>
      <!-- Main Row Styles -->
      <!-- Name -->
      <template #body-cell-name="props">
        <q-td :props="props">
          <div class="text-body1">
            <!-- Icons on left of row -->
            <q-icon
              v-if="props.row.format === 'folder'"
              class="mb-1"
              color="gray-800"
              left
              name="folder"
            />
            <q-icon
              v-else
              class="mb-1"
              color="gray-800"
              left
              name="insert_drive_file"
            />
            {{ props.value }}
            <!-- Zip button -->
            <q-btn
              v-if="loginState && !$q.platform.is.mobile && props.row.extension == '.zip' || props.row.extension == '.gz'"
              class="ml-1"
              :loading="unzipLoading"
              round
              outline
              size="xs"
              color="gray-800"
              icon="unarchive"
              @click.stop="unzip(props.row.name)"
            >
              <q-tooltip
                class="text-caption text-center text-body1"
                anchor="top middle"
                self="center middle"
                :offset="[20, 20]"
              >
                {{ $t('extract') }}
              </q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template>
      <!-- Buttons on right of row -->
      <template
        #body-cell-move="props"
        v-if="loginState && safeRoute"
      >
        <q-td
          :props="props"
          auto-width
        >
          <!-- Copy/Move -->
          <div>
            <q-btn
              round
              outline
              size="xs"
              color="gray-800"
              icon="drive_file_move_rtl"
              @click.stop="openFileSelector([{name:props.row.name, format:props.row.format}])"
            >
              <q-tooltip
                class="text-caption text-center text-body1"
                anchor="top middle"
                self="center middle"
                :offset="[20, 20]"
              >
                {{ $t('move_copy') }}
              </q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template>
      <!-- Rename -->
      <template
        #body-cell-rename="props"
        v-if="loginState && safeRoute"
      >
        <q-td
          :props="props"
          auto-width
        >
          <div>
            <q-btn
              round
              outline
              size="xs"
              color="gray-800"
              icon="drive_file_rename_outline"
              @click.stop
            >
              <q-popup-edit
                v-model="props.row.name"
                :title="$t('choose_name')"
                buttons
                auto-save
                v-slot="scope"
                @save="rename(props.row.name, newName)"
              >
                <q-input
                  ref="renameValid"
                  v-model="scope.value"
                  dense
                  autofocus
                  :rules="[(val) =>
                    !invalidCharacters.some(el => val.includes(el))
                    || $t('invalid_filemanager_string')]"
                  @keyup.enter="scope.set"
                  @update:model-value="newName = scope.value"
                />
              </q-popup-edit>
              <q-tooltip
                class="text-caption text-center text-body1"
                anchor="top middle"
                self="center middle"
                :offset="[20, 20]"
              >
                {{ $t('rename') }}
              </q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template>
      <!-- Delete -->
      <template
        #body-cell-delete="props"
        v-if="loginState && safeRoute"
      >
        <q-td
          :props="props"
          auto-width
        >
          <div>
            <q-btn
              round
              outline
              size="xs"
              color="gray-800"
              icon="delete"
              @click.stop="deleteFile([{name:props.row.name, format:props.row.format}])"
            >
              <q-tooltip
                class="text-caption text-center text-body1"
                anchor="top middle"
                self="center middle"
                :offset="[20, 20]"
              >
                {{ $t('delete') }}
              </q-tooltip>
            </q-btn>
          </div>
        </q-td>
      </template>
      <!-- Info -->
      <template #body-cell-info="props">
        <q-td
          :props="props"
          auto-width
        >
          <!-- Info menu for right of row -->
          <div class="desktop-only">
            <div v-if="props.row.format == 'file'">
              <q-icon
                size="xs"
                name="info"
                @click.stop
                @mouseover="fetchFileSize(props.row.name)"
              >
                <q-tooltip class="text-body1">
                  Size: {{ fileSize }}
                  <q-inner-loading :showing="loadingFileSize">
                    <q-spinner-gears
                      size="50px"
                      color="primary"
                    />
                  </q-inner-loading>
                </q-tooltip>
              </q-icon>
            </div>
          </div>
          <!-- Mobile menu for right of row -->
          <div
            v-if="loginState && safeRoute"
            class="mobile-only"
          >
            <q-btn
              round
              size="xs"
              flat
              icon="menu"
              @click.stop
            >
              <q-menu
                auto-close
                class="text-center"
              >
                <q-list style="min-width: 100px">
                  <q-item
                    clickable
                    v-if="props.row.extension == '.zip' || props.row.extension == '.gz'"
                  >
                    <q-item-section
                      @click="unzip(props.row.name)"
                    >
                      {{ $t('extract') }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section
                      @click="openFileSelector([{name:props.row.name, format:props.row.format}])"
                    >
                      {{ $t('move_copy') }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section
                      @click="mobileRenameFile(props.row.name)"
                    >
                      {{ $t('rename') }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section
                      @click="deleteFile([{name:props.row.name, format:props.row.format}])"
                    >
                      {{ $t('delete') }}
                    </q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </div>
        </q-td>
      </template>
    </q-table>
    <!-- File Selector -->
    <q-dialog
      v-model="fileSelector"
    >
      <q-card style="max-width: 95vw;">
        <q-card-section class="row items-center justify-center">
          <q-table
            v-if="selectorRows"
            table-style="width: 75vw;"
            hide-bottom
            flat
            :dense="!$q.platform.is.mobile"
            square
            wrap-cells
            :no-data-label="$t('empty_folder')"
            :no-results-label="$t('empty_folder')"
            :loading="loading"
            :rows-per-page-options="[0]"
            :rows="selectorRows"
            :columns="selectorColumns"
            filter="folder"
            :filter-method="filterFiles"
            row-key="name"
            @row-click="onSelectorRowClick"
          >
            <!-- Header -->
            <template #top-left>
              <div>
                {{ $t('select_folder') }}
              </div>
              <div class="mt-2">
                <q-btn
                  icon="arrow_back_ios"
                  color="gray-800"
                  outline
                  rounded
                  size="sm"
                  :disable="!selectorObjPath[0]"
                  @click="selectorObjPath.pop(), updateSelectorRows()"
                />
              </div>
            </template>
            <!-- Name -->
            <template #body-cell-name="props">
              <q-td :props="props">
                <div class="text-body1">
                  <q-icon
                    class="mb-1"
                    color="gray-800"
                    left
                    name="folder"
                  />
                  {{ props.value }}
                </div>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            class="mr-3"
            flat
            :label="$t('cancel')"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            :label="$t('move')"
            color="primary"
            v-close-popup
            @click="moveCopyItem('move')"
          />
          <q-btn
            flat
            :label="$t('copy')"
            color="primary"
            v-close-popup
            @click="moveCopyItem('copy')"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script lang="ts">
import Axios from 'app/node_modules/axios'
import { useQuasar, openURL } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const route = useRoute()
    const $router = useRouter()
    const $store = useStore()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    // Get api from store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    const checkRowExistence = nameParam => rows.value.some(({ name }) => name === nameParam)
    const chosenPath = ref<string>('')
    const currentPath = ref<any>('')
    const fileSelector = ref<boolean>(false)
    const fileSize = ref<number>(0)
    const invalidCharacters = ref<Array<any>>([
      '<', '>', '%', '{', '}', '|', '\\', '^', '`', '$', '#'
    ])
    const loading = ref<boolean>(true)
    const loadingFileSize = ref<boolean>(false)
    const loginState = $store.getters.isAuthenticated
    const loginToken = ref<string>(Axios.defaults.headers.common.Authorization)
    const renameValid = ref()
    const rootPath = ref<string>()
    const rows = ref<any>(null)
    const objPath = ref<Array<any>>([])
    const safeRoute = ref<boolean>(false)
    const selected = ref<Array<any>>([])
    const selectedItem = ref<Array<any>>([])
    const selectorObjPath = ref<Array<any>>([])
    const selectorRows = ref<any>(null)
    const unzipLoading = ref<boolean>(false)
    const visibleColumns = ref<Array<any>>([])
    const windowHostname = ref<string>(window.location.origin)

    const columns = [
      {
        name: 'name',
        required: true,
        label: t('name'),
        align: 'left',
        field: row => row.name,
        format: val => `${val}`
      },
      { name: 'move', field: 'move' },
      { name: 'rename', field: 'rename' },
      { name: 'delete', field: 'delete' },
      { name: 'info', field: 'info' },
      { name: 'extension', field: 'extension' }
    ]

    const selectorColumns = [
      {
        name: 'name',
        required: true,
        label: t('name'),
        align: 'left',
        field: row => row.name,
        format: val => `${val}`
      }
    ]

    onMounted(async () => {
      $q.loading.show({
        delay: 500 // ms
      })
      if ($q.platform.is.mobile) {
        visibleColumns.value = ['info']
      } else {
        visibleColumns.value = ['move', 'rename', 'delete', 'info']
      }
      if (route.params.data) {
        chosenPath.value = `${route.params.data}/`
      }
      if (loginState) {
        rootPath.value = `/app/storage/${chosenPath.value}`
      } else if (!loginState && chosenPath.value) {
        rootPath.value = `/app/storage/${chosenPath.value}`
      } else {
        rootPath.value = '/app/storage/fileshare/'
      }
      await updateRows()
      $q.loading.hide()
    })

    function checkCharacters (files) {
      return files.filter(file => !invalidCharacters.value.some(el => file.name.includes(el)))
    }

    function checkUploadOverwrite (files) {
      for (let i = 0; i < files.length; i++) {
        if (rows.value.some(({ name }) => name === files[i].name)) {
          $q.notify({
            type: 'warning',
            message: t('upload_files_exist')
          })
        }
      }
    }

    async function confirmOverwrite (item, rows) {
      const arrayItem = JSON.parse(JSON.stringify(item))
      const arrayRow = JSON.parse(JSON.stringify(rows))

      for (let i = 0; i < arrayItem.length; i++) {
        if (arrayRow.some(({ name }) => name === arrayItem[i].name)) {
          if (await new Promise(resolve => $q.dialog({
            title: t('confirm'),
            message: t('overwrite_warning'),
            cancel: true
          }).onOk(() => resolve(true)).onCancel(() => resolve(false)))) {
            return true
          } else {
            return false
          }
        }
      } return true
    }

    function deleteFile (itemObj) {
      $q.dialog({
        title: t('confirm'),
        message: t('confirm_delete'),
        cancel: true
      }).onOk(async () => {
        await Axios.post(`${api.value}/v1/filemanager/delete`, {
          path: objPath.value,
          object: itemObj,
          root: rootPath.value
        })
        selected.value = []
        await updateRows()
        notifyComplete()
      })
    }

    async function fetchFileSize (itemFile) {
      fileSize.value = 0
      loadingFileSize.value = true
      await Axios.post(`${api.value}/v1/filemanager/file_size`, {
        path: objPath.value,
        item: itemFile,
        root: rootPath.value
      }).then((response) => {
        fileSize.value = response.data.size
      })
      loadingFileSize.value = false
    }

    function filterFiles (rows, terms) {
      return rows.filter(row => row.format === terms)
    }

    function mobileRenameFile (currentName) {
      $q.dialog({
        title: t('select_folder'),
        message: t('select_folder'),
        prompt: {
          model: '',
          isValid: val => val !== ''
        },
        cancel: true
      }).onOk(data => {
        if (invalidCharacters.value.some(el => data.includes(el))) {
          $q.notify({
            type: 'negative',
            message: t('invalid_filemanager_string')
          })
        } else {
          rename(currentName, data)
        }
      })
    }

    async function moveCopyItem (action) {
      if (await confirmOverwrite(selectedItem.value, selectorRows.value)) {
        if (action === 'move') {
          await Axios.post(`${api.value}/v1/filemanager/move`, {
            fromPath: objPath.value,
            toPath: selectorObjPath.value,
            object: selectedItem.value,
            root: rootPath.value
          })
        } else if (action === 'copy') {
          await Axios.post(`${api.value}/v1/filemanager/copy`, {
            fromPath: objPath.value,
            toPath: selectorObjPath.value,
            object: selectedItem.value,
            root: rootPath.value
          })
        }
        selected.value = []
        await updateRows()
        notifyComplete()
      }
    }

    function newFolderPrompt () {
      $q.dialog({
        title: t('choose_name'),
        message: t('choose_name'),
        prompt: {
          model: '',
          isValid: val => val !== ''
        },
        cancel: true
      }).onOk(async data => {
        if (invalidCharacters.value.some(el => data.includes(el))) {
          $q.notify({
            type: 'negative',
            message: t('invalid_filemanager_string')
          })
        } else {
          if (checkRowExistence(data)) {
            $q.notify({
              type: 'negative',
              message: t('item_already_exists')
            })
          } else {
            await Axios.post(`${api.value}/v1/filemanager/newfolder`, {
              path: objPath.value,
              directory: data,
              root: rootPath.value
            })
            await updateRows()
            notifyComplete()
          }
        }
      })
    }

    function notifyComplete () {
      $q.notify({
        type: 'positive',
        icon: 'done',
        timeout: 100
      })
    }

    function onUploaderRejected (rejectedEntries) {
      $q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} ${t('invalid_upload_string')}`
      })
    }

    function onRowClick (_evt, row) {
      const index = row.name.lastIndexOf('.') as number
      const ePub = index > 0 && row.name.substring(index + 1).toLowerCase() === 'epub'
      if (row.format === 'file') {
        const encodedCurrentPath = encodeURIComponent(currentPath.value)
        const encodedRowName = encodeURIComponent(row.name)
        if (currentPath.value) {
          if (ePub) {
            $router.push(`/epub_reader/?url=${windowHostname.value}/storage/${encodedCurrentPath}/${encodedRowName}`)
          } else {
            openURL(`/storage/${encodedCurrentPath}/${encodedRowName}`)
          }
        } else {
          if (ePub) {
            $router.push(`/epub_reader/?url=${windowHostname.value}/storage/${encodedRowName}`)
          } else {
            openURL(`/storage/${encodedRowName}`)
          }
        }
      } else if (row.format === 'folder') {
        objPath.value.push(row.name)
        selected.value = []
        updateRows().then(() => {
          // Auto open files starting with --auto-open
          if (!loginState) {
            const stringExists = rows.value.findIndex(({ name }) => name.substring(0, 11) === '--auto-open')
            if (stringExists > -1) {
              const fileName = rows.value[stringExists].name
              const index = fileName.lastIndexOf('.') as number
              const ePub = fileName.substring(index + 1).toLowerCase() === 'epub'
              const encodedCurrentPath = encodeURIComponent(currentPath.value)
              const encodedRowName = encodeURIComponent(fileName)
              if (encodedCurrentPath) {
                if (ePub) {
                  $router.push(`/epub_reader/?url=${windowHostname.value}/storage/${encodedCurrentPath}/${encodedRowName}`)
                } else {
                  openURL(`/storage/${encodedCurrentPath}/${encodedRowName}`)
                }
              } else {
                if (ePub) {
                  $router.push(`/epub_reader/?url=${windowHostname.value}/storage/${encodedRowName}`)
                } else {
                  openURL(`/storage/${encodedRowName}`)
                }
              }
            }
          }
        })
      }
    }

    function onSelectorRowClick (_evt, row) {
      selectorObjPath.value.push(row.name)
      updateSelectorRows()
    }

    function openFileSelector (obj) {
      selectedItem.value = obj
      updateSelectorRows()
      fileSelector.value = true
    }

    async function rename (currentName, newName) {
      if (checkRowExistence(newName)) {
        $q.notify({
          type: 'negative',
          message: t('item_already_exists')
        })
      } else {
        await Axios.post(`${api.value}/v1/filemanager/rename`, {
          path: objPath.value,
          from: currentName,
          to: newName,
          root: rootPath.value
        })
        notifyComplete()
      }
      updateRows()
    }

    async function unzip (fileName) {
      unzipLoading.value = true
      await Axios.post(`${api.value}/v1/filemanager/unzip`, {
        file: fileName,
        path: objPath.value,
        root: rootPath.value
      })
      await updateRows()
      notifyComplete()
      unzipLoading.value = false
    }

    async function updateRows () {
      loading.value = true
      if (objPath.value.length === 0 && rootPath.value === '/app/storage/') {
        safeRoute.value = false
      } else {
        safeRoute.value = true
      }
      await Axios.post(`${api.value}/v1/filemanager/list`, {
        path: objPath.value,
        root: rootPath.value
      }).then((response) => {
        rows.value = response.data.rows
        currentPath.value = response.data.path
        selectorObjPath.value = []
        selectorObjPath.value = selectorObjPath.value.concat(objPath.value)
      }).catch(function (error) {
        console.log(error)
        if (objPath.value !== []) {
          objPath.value = []
          updateRows()
        }
        $q.notify({ type: 'negative', message: t('error') })
      })
      loading.value = false
    }

    async function updateSelectorRows () {
      loading.value = true
      await Axios.post(`${api.value}/v1/filemanager/list`, {
        path: selectorObjPath.value,
        root: rootPath.value
      }).then((response) => {
        selectorRows.value = response.data.rows
      }).catch(function (error) {
        console.log(error)
        $q.notify({ type: 'negative', message: t('error') })
      })
      loading.value = false
    }

    async function uploadFailed (response) {
      if (response.xhr.status === 401) {
        await $router.replace('/login')
      } else {
        $q.notify({ type: 'negative', message: t('error') })
      }
    }

    return {
      api,
      checkCharacters,
      checkUploadOverwrite,
      columns,
      deleteFile,
      fetchFileSize,
      fileSelector,
      fileSize,
      filter: ref(''),
      filterFiles,
      invalidCharacters,
      loading,
      loadingFileSize,
      loginState,
      loginToken,
      mobileRenameFile,
      moveCopyItem,
      newFolderPrompt,
      newName: ref<any>(''),
      objPath,
      onUploaderRejected,
      onRowClick,
      onSelectorRowClick,
      openFileSelector,
      rename,
      renameValid,
      rootPath,
      rows,
      searchTable: ref(false),
      safeRoute,
      selected,
      selectedItem,
      selectorColumns,
      selectorObjPath,
      selectorRows,
      unzip,
      unzipLoading,
      updateRows,
      updateSelectorRows,
      uploaderDialog: ref(false),
      uploadFailed,
      visibleColumns
    }
  }
})

</script>

<style scoped>

</style>