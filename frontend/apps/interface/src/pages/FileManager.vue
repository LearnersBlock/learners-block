<template>
  <q-page class="items-center p-3">
    <!-- Home Button -->
    <q-btn
      v-if="rows"
      rounded
      size="sm"
      color="white"
      text-color="primary"
      class="mt-1 mb-1 text-weight-bold"
      outline
      :label="$t('back')"
      icon="arrow_back"
      @click="$router.back()"
    />
    <q-table
      v-if="rows"
      v-model:selected="selected"
      table-style="width: 90vw;"
      flat
      :dense="$q.screen.gt.sm"
      wrap-cells
      :loading="loading"
      :rows="rows"
      :rows-per-page-options="[50, 75, 100, 0]"
      :columns="columns"
      :no-data-label="
        $route.params.data === 'library' && !objPath[0]
          ? $t('library_empty')
          : $t('empty_folder')
      "
      :no-results-label="$t('no_results_found')"
      row-key="name"
      :selection="loginState && $q.screen.gt.sm ? 'multiple' : 'none'"
      :filter="filter"
      :visible-columns="visibleColumns"
      @row-click="onRowClick"
    >
      <!-- Toolbar -->
      <template #top="props">
        <div
          class="flex row full-width row reverse-wrap justify-between items-center"
        >
          <div class="col-auto m-1 mt-2">
            <q-breadcrumbs v-if="!objPath[0]">
              <q-breadcrumbs-el
                v-ripple
                class="cursor-pointer mb-1"
                icon="home"
                clickable
              />
            </q-breadcrumbs>
            <q-breadcrumbs v-else>
              <q-breadcrumbs-el
                v-ripple
                class="cursor-pointer mb-1"
                icon="home"
                clickable
                color="gray-800"
                @click="objPath.splice(0, objPath.length), updateRows()"
              />
              <q-breadcrumbs-el
                v-for="path in objPath"
                :key="path"
                v-ripple
                class="cursor-pointer"
                clickable
                :label="path"
                @click="
                  ;(objPath.length = objPath.indexOf(path) + 1), updateRows()
                "
              />
            </q-breadcrumbs>
          </div>
          <div class="col-auto ml-3 mb-1">
            <div>
              <q-btn
                v-if="loginState"
                class="mr-2"
                icon="create_new_folder"
                color="gray-800"
                outline
                rounded
                size="sm"
                @click="newFolderPrompt"
              >
                <q-tooltip
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('new_folder') }}
                </q-tooltip>
              </q-btn>
              <q-btn
                v-if="loginState && $q.screen.gt.sm"
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
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('move_copy') }}
                </q-tooltip>
              </q-btn>
              <q-btn
                v-if="loginState"
                class="mr-2"
                icon="upload"
                color="gray-800"
                outline
                rounded
                size="sm"
                @click="uploaderDialog = true"
              >
                <q-tooltip
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('upload') }}
                </q-tooltip>
              </q-btn>
              <q-dialog v-model="uploaderDialog">
                <q-uploader
                  style="max-width: 300px"
                  :label="$t('upload')"
                  color="white"
                  text-color="black"
                  multiple
                  flat
                  no-thumbnails
                  with-credentials
                  :readonly="delayUpload"
                  :filter="checkCharacters"
                  :url="api + '/v1/filemanager/upload'"
                  :headers="[
                    { name: 'rootPath', value: rootPath },
                    { name: 'savePath', value: JSON.stringify(objPath) },
                    { name: 'Authorization', value: loginToken }
                  ]"
                  @uploaded="updateRows()"
                  @failed="uploadFailed"
                  @rejected="onUploaderRejected"
                  @added="checkUploadOverwrite"
                />
              </q-dialog>
              <q-btn
                v-if="loginState && $q.screen.gt.sm"
                class="mr-2"
                size="sm"
                color="gray-800"
                rounded
                outline
                icon="delete"
                @click="deleteFile(JSON.parse(JSON.stringify(selected)))"
              >
                <q-tooltip
                  class="text-caption text-center"
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
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('filter') }}
                </q-tooltip>
              </q-btn>
              <q-btn
                v-if="$q.screen.gt.sm"
                class="q-ml-md"
                flat
                round
                dense
                :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
                @click="props.toggleFullscreen()"
              >
                <q-tooltip
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('full_screen') }}
                </q-tooltip>
              </q-btn>
              <q-input
                v-if="searchTable"
                v-model="filter"
                class="ml-3"
                dense
                debounce="300"
                hide-bottom-space
                :placeholder="$t('filter')"
              >
                <template #append>
                  <q-icon
                    name="close"
                    class="cursor-pointer"
                    @click="filter = ''"
                  />
                </template>
              </q-input>
            </div>
          </div>
        </div>
      </template>
      <!-- Main Row Styles -->
      <!-- Name -->
      <template #body-cell-name="props">
        <q-td :props="props">
          <div>
            <!-- Icons on left of row -->
            <q-slide-item
              right-color="red"
              @action="resetSlide"
              @right="
                deleteFile([{ name: props.row.name, format: props.row.format }])
              "
            >
              <template #right>
                <q-icon name="delete" />
              </template>
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
                v-if="
                  loginState &&
                  $q.screen.gt.sm &&
                  (props.row.extension == '.zip' ||
                    props.row.extension == '.gz')
                "
                class="ml-2"
                :loading="
                  unzipLoading && unzipLoadingFileName === props.row.name
                "
                round
                outline
                size="xs"
                color="gray-800"
                icon="unarchive"
                @click.stop="unzip(props.row.name)"
              >
                <q-tooltip
                  class="text-caption text-center"
                  anchor="top middle"
                  self="center middle"
                  :offset="[20, 20]"
                >
                  {{ $t('extract') }}
                </q-tooltip>
              </q-btn>
            </q-slide-item>
          </div>
        </q-td>
      </template>
      <!-- Buttons on right of row -->
      <template v-if="loginState" #body-cell-move="props">
        <q-td :props="props" auto-width>
          <!-- Copy/Move -->
          <div>
            <q-btn
              round
              outline
              size="xs"
              color="gray-800"
              icon="drive_file_move_rtl"
              @click.stop="
                openFileSelector([
                  { name: props.row.name, format: props.row.format }
                ])
              "
            >
              <q-tooltip
                class="text-caption text-center"
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
      <template v-if="loginState" #body-cell-rename="props">
        <q-td :props="props" auto-width>
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
                v-slot="scope"
                v-model="props.row.name"
                :title="$t('enter_name')"
                buttons
                auto-save
                @save="rename(props.row.name, newName)"
              >
                <q-input
                  v-model="scope.value"
                  dense
                  autofocus
                  hide-bottom-space
                  :rules="[
                    (val) =>
                      !invalidCharacters.some((el) => val.includes(el)) ||
                      $t('invalid_filemanager_string')
                  ]"
                  @keyup.enter="scope.set()"
                  @update:model-value="newName = scope.value"
                />
              </q-popup-edit>
              <q-tooltip
                class="text-caption text-center"
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
      <template v-if="loginState" #body-cell-delete="props">
        <q-td :props="props" auto-width>
          <div>
            <q-btn
              round
              outline
              size="xs"
              color="gray-800"
              icon="delete"
              @click.stop="
                deleteFile([{ name: props.row.name, format: props.row.format }])
              "
            >
              <q-tooltip
                class="text-caption text-center"
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
        <q-td :props="props" auto-width>
          <!-- Info menu for right of row -->
          <div v-if="$q.screen.gt.sm" class="touch-hide">
            <div v-if="props.row.format == 'file'">
              <q-icon
                size="xs"
                name="info"
                @click.stop
                @mouseover="fetchFileSize(props.row.name)"
              >
                <q-tooltip class="text-caption">
                  Size: {{ fileSize }}
                  <q-inner-loading :showing="loadingFileSize">
                    <q-spinner-gears size="50px" color="primary" />
                  </q-inner-loading>
                </q-tooltip>
              </q-icon>
            </div>
          </div>
          <!-- Mobile menu for right of row -->
          <div v-if="loginState && !$q.screen.gt.sm">
            <q-btn
              :loading="unzipLoading && unzipLoadingFileName === props.row.name"
              round
              size="xs"
              flat
              icon="menu"
              @click.stop
            >
              <q-menu auto-close class="text-center">
                <q-list style="min-width: 100px">
                  <q-item
                    v-if="
                      props.row.extension == '.zip' ||
                      props.row.extension == '.gz'
                    "
                    clickable
                  >
                    <q-item-section @click="unzip(props.row.name)">
                      {{ $t('extract') }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section
                      @click="
                        openFileSelector([
                          { name: props.row.name, format: props.row.format }
                        ])
                      "
                    >
                      {{ $t('move_copy') }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section @click="mobileRenameFile(props.row.name)">
                      {{ $t('rename') }}
                    </q-item-section>
                  </q-item>
                  <q-item clickable>
                    <q-item-section
                      @click="
                        deleteFile([
                          { name: props.row.name, format: props.row.format }
                        ])
                      "
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
    <q-dialog v-model="fileSelector" @hide="selectorRows = []">
      <q-card style="max-width: 95vw">
        <q-card-section class="row items-center justify-center">
          <q-table
            table-style="width: 75vw;"
            hide-bottom
            flat
            :dense="$q.screen.gt.sm"
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
                  icon="keyboard_arrow_up"
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
                <div>
                  <q-icon class="mb-1" color="gray-800" left name="folder" />
                  {{ props.value }}
                </div>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn
            v-close-popup
            class="mr-3"
            flat
            :label="$t('cancel')"
            color="primary"
          />
          <q-btn
            v-close-popup
            flat
            :label="$t('move')"
            color="primary"
            @click="moveCopyItem('move')"
          />
          <q-btn
            v-close-popup
            flat
            :label="$t('copy')"
            color="primary"
            @click="moveCopyItem('copy')"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script lang="ts">
import Axios from 'axios'
import { useQuasar } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'IntFileManager',
  setup() {
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

    const checkRowExistence = (nameParam) =>
      rows.value.some(({ name }) => name === nameParam)
    const currentPath = ref<string>('')
    const delayUpload = ref<boolean>(false)
    const fileSelector = ref<boolean>(false)
    const fileSize = ref<number>(0)
    const invalidCharacters = ref<Array<any>>(['/', '\\0'])
    const loading = ref<boolean>(true)
    const loadingFileSize = ref<boolean>(false)
    const loginState = $store.getters.isAuthenticated
    const loginToken = ref<string | number | boolean>(
      Axios.defaults.headers.common.Authorization
    )
    const rootPath = ref<any>()
    const rows = ref<Array<any>>([])
    const objPath = ref<Array<any>>([])
    const selected = ref<Array<any>>([])
    const selectedItem = ref<Array<any>>([])
    const selectorObjPath = ref<Array<any>>([])
    const selectorRows = ref<Array<any>>([])
    const unzipLoading = ref<boolean>(false)
    const unzipLoadingFileName = ref<string>('')
    const visibleColumns = ref<Array<any>>([])
    const windowHostname = ref<string>(window.location.origin)

    const columns = computed(() => [
      {
        name: 'name',
        required: true,
        label: t('name'),
        align: 'left',
        field: (row) => row.name,
        format: (val) => `${val}`
      },
      { name: 'move', field: 'move' },
      { name: 'rename', field: 'rename' },
      { name: 'delete', field: 'delete' },
      { name: 'info', field: 'info' },
      { name: 'extension', field: 'extension' }
    ]) as any

    const selectorColumns = computed(() => [
      {
        name: 'name',
        required: true,
        label: t('name'),
        align: 'left',
        field: (row) => row.name,
        format: (val) => `${val}`
      }
    ]) as any

    // Adjust visible columns when screen is rotated
    watch(
      () => $q.screen.gt.sm,
      (size) => {
        if (size) {
          visibleColumns.value = ['move', 'rename', 'delete', 'info']
        } else {
          visibleColumns.value = ['info']
        }
      }
    )

    onMounted(async () => {
      $q.loading.show()

      if (route.params.data) {
        rootPath.value = route.params.data
      } else {
        rootPath.value = 'fileshare'
      }
      if ($q.screen.gt.sm) {
        visibleColumns.value = ['move', 'rename', 'delete', 'info']
      } else {
        visibleColumns.value = ['info']
      }

      await updateRows()

      // Auto open files starting with --auto-open
      if (!loginState) {
        checkAutoOpenFile()
      }
      $q.loading.hide()
    })

    function checkAutoOpenFile() {
      const stringExists = rows.value.findIndex(
        ({ name }) => name.substring(0, 11) === '--auto-open'
      )
      if (stringExists > -1) {
        const fileName = rows.value[stringExists].name
        const index = fileName.lastIndexOf('.') as number
        const ePub = fileName.substring(index + 1).toLowerCase() === 'epub'
        const encodedCurrentPath = encodeURIComponent(currentPath.value)
        const encodedRowName = encodeURIComponent(
          fileName as string | number | boolean
        )
        if (encodedCurrentPath) {
          if (ePub) {
            void $router.push(
              `/epub_reader/?url=${windowHostname.value}/storage/${encodedCurrentPath}/${encodedRowName}`
            )
          } else {
            // Uses window.open to open a new window. Otherwise a user hits the back button to return
            // to the FileManager from the opened item and loses their folder position.
            window.open(
              `/storage/${encodedCurrentPath}/${encodedRowName}`,
              '_blank'
            )
          }
        } else {
          if (ePub) {
            void $router.push(
              `/epub_reader/?url=${windowHostname.value}/storage/${encodedRowName}`
            )
          } else {
            window.open(`/storage/${encodedRowName}`, '_blank')
          }
        }
      }
    }

    function checkCharacters(files) {
      return files.filter(
        (file) => !invalidCharacters.value.some((el) => file.name.includes(el))
      )
    }

    function checkUploadOverwrite(files) {
      const itemCheck = files.filter((obj) => {
        return rows.value.some(({ name }) => name === obj.name)
      })

      if (itemCheck.length > 0) {
        delayUpload.value = true
        $q.notify({
          actions: [
            {
              label: t('close'),
              color: 'black',
              handler: () => {
                /* ... */
              }
            }
          ],
          onDismiss: () => {
            delayUpload.value = false
          },
          timeout: 0,
          type: 'warning',
          position: 'center',
          message: t('upload_files_exist')
        })
      }
    }

    async function confirmOverwrite(item, rows) {
      // Check if item already exists
      const itemCheck = item.filter((obj) => {
        return rows.some(({ name }) => name === obj.name)
      })

      // If item exists show warning
      if (itemCheck.length > 0) {
        if (
          await new Promise((resolve) =>
            $q
              .dialog({
                title: t('confirm'),
                message: t('overwrite_warning'),
                cancel: true
              })
              .onOk(() => resolve(true))
              .onCancel(() => resolve(false))
          )
        ) {
          return true
        } else {
          return false
        }
      } else {
        return true
      }
    }

    function deleteFile(itemObj) {
      $q.dialog({
        title: t('confirm'),
        message: t('confirm_delete'),
        cancel: true
      }).onOk(() => {
        void Axios.post(`${api.value}/v1/filemanager/delete`, {
          path: objPath.value,
          object: itemObj,
          root: rootPath.value
        }).then(async () => {
          selected.value = []
          await updateRows()
          notifyComplete()
        })
      })
    }

    async function fetchFileSize(itemFile) {
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

    function filterFiles(rows, terms) {
      return rows.filter((row) => row.format === terms)
    }

    function mobileRenameFile(currentName) {
      $q.dialog({
        title: t('rename'),
        message: t('enter_name'),
        prompt: {
          model: currentName,
          isValid: (val) => val !== ''
        },
        cancel: true
      }).onOk((data) => {
        if (invalidCharacters.value.some((el) => data.includes(el))) {
          $q.notify({
            type: 'negative',
            message: t('invalid_filemanager_string')
          })
        } else {
          void rename(currentName, data)
        }
      })
    }

    async function moveCopyItem(action) {
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

    function newFolderPrompt() {
      $q.dialog({
        title: t('new_folder'),
        message: t('enter_name'),
        prompt: {
          model: '',
          isValid: (val) => val !== ''
        },
        cancel: true
      }).onOk((data) => {
        if (invalidCharacters.value.some((el) => data.includes(el))) {
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
            void Axios.post(`${api.value}/v1/filemanager/new_folder`, {
              path: objPath.value,
              directory: data,
              root: rootPath.value
            }).then(async () => {
              await updateRows()
              notifyComplete()
            })
          }
        }
      })
    }

    function notifyComplete() {
      $q.notify({
        type: 'positive',
        icon: 'done',
        timeout: 100
      })
    }

    function onRowClick(_evt, row) {
      const index = row.name.lastIndexOf('.') as number
      const ePub =
        index > 0 && row.name.substring(index + 1).toLowerCase() === 'epub'
      if (row.format === 'file') {
        const encodedCurrentPath = encodeURIComponent(currentPath.value)
        const encodedRowName = encodeURIComponent(
          row.name as string | number | boolean
        )
        if (currentPath.value) {
          if (ePub) {
            void $router.push(
              `/epub_reader/?url=${windowHostname.value}/storage/${encodedCurrentPath}/${encodedRowName}`
            )
          } else {
            window.open(
              `/storage/${encodedCurrentPath}/${encodedRowName}`,
              '_blank'
            )
          }
        } else {
          if (ePub) {
            void $router.push(
              `/epub_reader/?url=${windowHostname.value}/storage/${encodedRowName}`
            )
          } else {
            window.open(`/storage/${encodedRowName}`, '_blank')
          }
        }
      } else if (row.format === 'folder') {
        objPath.value.push(row.name)
        selected.value = []
        void updateRows().then(() => {
          // Auto open files starting with --auto-open
          if (!loginState) {
            checkAutoOpenFile()
          }
        })
      }
    }

    function onSelectorRowClick(_evt, row) {
      selectorObjPath.value.push(row.name)
      void updateSelectorRows()
    }

    function onUploaderRejected(rejectedEntries) {
      $q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} ${t('invalid_upload_string')}`
      })
    }

    function openFileSelector(obj) {
      selectedItem.value = obj
      selectorObjPath.value = []
      selectorObjPath.value = selectorObjPath.value.concat(objPath.value)
      void updateSelectorRows()
      fileSelector.value = true
    }

    async function rename(currentName, newName) {
      if (checkRowExistence(newName)) {
        $q.notify({
          type: 'negative',
          message: t('item_already_exists')
        })
      } else if (invalidCharacters.value.some((el) => newName.includes(el))) {
        $q.notify({
          type: 'negative',
          message: t('invalid_filemanager_string')
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
      void updateRows()
    }

    async function unzip(fileName) {
      unzipLoadingFileName.value = fileName
      unzipLoading.value = true
      await Axios.post(`${api.value}/v1/filemanager/unzip`, {
        file: fileName,
        path: objPath.value,
        root: rootPath.value
      }).then((response) => {
        if (response.data.message === 'error') {
          $q.notify({ type: 'negative', message: t('error') })
        } else {
          $q.notify({
            type: 'positive',
            message: `${t('extracted_to')} ${response.data.new_path}`
          })
        }
      })
      await updateRows()
      unzipLoading.value = false
    }

    async function updateRows() {
      loading.value = true
      await Axios.post(`${api.value}/v1/filemanager/list`, {
        path: objPath.value,
        root: rootPath.value
      })
        .then((response) => {
          rows.value = response.data.rows
          currentPath.value = response.data.path
          selectorObjPath.value = []
          selectorObjPath.value = selectorObjPath.value.concat(objPath.value)
        })
        .catch(function (error) {
          console.log(error)
          if (objPath.value !== []) {
            objPath.value = []
            void updateRows()
          }
          $q.notify({ type: 'negative', message: t('error') })
        })
      loading.value = false
    }

    async function updateSelectorRows() {
      loading.value = true
      await Axios.post(`${api.value}/v1/filemanager/list`, {
        path: selectorObjPath.value,
        root: rootPath.value
      }).then((response) => {
        selectorRows.value = response.data.rows
      })
      loading.value = false
    }

    async function uploadFailed(response) {
      if (response.xhr.status === 401) {
        $q.notify({ type: 'negative', message: t('login_again') })
        await $router.replace('/settings')
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
      delayUpload,
      fetchFileSize,
      fileSelector,
      fileSize,
      filter: ref<string>(),
      filterFiles,
      invalidCharacters,
      loading,
      loadingFileSize,
      loginState,
      loginToken,
      mobileRenameFile,
      moveCopyItem,
      newFolderPrompt,
      newName: ref<string>(),
      objPath,
      onUploaderRejected,
      onRowClick,
      onSelectorRowClick,
      openFileSelector,
      rename,
      resetSlide({ reset }) {
        reset()
      },
      rootPath,
      rows,
      searchTable: ref<boolean>(false),
      selected,
      selectorColumns,
      selectorObjPath,
      selectorRows,
      unzip,
      unzipLoading,
      unzipLoadingFileName,
      updateRows,
      updateSelectorRows,
      uploaderDialog: ref<boolean>(false),
      uploadFailed,
      visibleColumns
    }
  }
})
</script>

<style scoped></style>
