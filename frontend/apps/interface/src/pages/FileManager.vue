<template>
  <q-page class="items-center p-3 text-body1">
    <div class="mb-1">
      <q-breadcrumbs v-if="!objPath[0]">
        <q-breadcrumbs-el
          class="cursor-pointer"
          icon="home"
          label="Home"
        />
      </q-breadcrumbs>
      <q-breadcrumbs v-else>
        <q-breadcrumbs-el
          class="cursor-pointer"
          icon="home"
          label="Home"
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
    <q-table
      v-if="rows"
      table-style="width: 90vw;"
      flat
      :rows="rows"
      :rows-per-page-options="[10, 20, 50, 100]"
      :columns="columns"
      row-key="name"
      :selection="loginState ? 'multiple' : 'none'"
      v-model:selected="selected"
      :filter="filter"
      :visible-columns="visibleColumns"
      @row-click="onRowClick"
    >
      <!-- Back Button -->
      <template #top-left>
        <div>
          <div>
            {{ $t('file_manager') }}
          </div>
          <div class="mt-2">
            <q-btn
              class="mr-1"
              icon="arrow_back_ios"
              color="gray-800"
              outline
              rounded
              size="sm"
              :disable="!objPath[0]"
              @click="objPath.pop(), updateRows()"
            />
          </div>
        </div>
      </template>
      <!-- Toolbar -->
      <template #top-right="props">
        <div v-if="loginState && safeRoute">
          <q-btn
            class="mr-1"
            icon="create_new_folder"
            color="gray-800"
            outline
            rounded
            size="sm"
            @click="newFolderPrompt"
          />
          <q-btn
            class="mr-1"
            icon="drive_file_move_rtl"
            color="gray-800"
            outline
            rounded
            size="sm"
            :disable="!JSON.parse(JSON.stringify(selected))[0]"
            @click="openFileSelector(JSON.parse(JSON.stringify(selected)))"
          />
          <q-btn
            class="mr-1"
            icon="upload"
            color="gray-800"
            outline
            rounded
            size="sm"
            @click="uploaderDialog = true"
          />
          <q-dialog
            v-model="uploaderDialog"
          >
            <q-uploader
              style="max-width: 300px"
              label="Upload"
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
              @rejected="onRejected"
              @added="checkUploadOverwrite"
            />
          </q-dialog>
          <q-btn
            class="mr-1"
            size="sm"
            color="gray-800"
            rounded
            outline
            icon="delete"
            @click="deleteFile(JSON.parse(JSON.stringify(selected)))"
          />
        </div>
        <q-btn
          class="mr-1"
          icon="search"
          color="gray-800"
          outline
          rounded
          size="sm"
          @click="searchTable = true"
        />
        <q-input
          v-if="searchTable"
          class="ml-2"
          dense
          debounce="300"
          hide-bottom-space
          v-model="filter"
          placeholder="Search"
        />
        <q-btn
          flat
          round
          dense
          :icon="props.inFullscreen ? 'fullscreen_exit' : 'fullscreen'"
          @click="props.toggleFullscreen"
          class="q-ml-md"
        />
      </template>
      <!-- Name -->
      <template #body-cell-name="props">
        <q-td :props="props">
          <div class="text-body1">
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
            <q-btn
              v-if="loginState && props.row.extension == '.zip' || props.row.extension == '.gz'"
              :loading="unzipLoading"
              round
              outline
              size="xs"
              color="gray-800"
              icon="unarchive"
              @click.stop="unzip(props.row.name)"
            />
          </div>
        </q-td>
      </template>
      <!-- Copy/Move -->
      <template
        #body-cell-move="props"
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
              icon="drive_file_move_rtl"
              @click.stop="openFileSelector([{name:props.row.name, format:props.row.format}])"
            />
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
                title="Enter a new name"
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
                    || $t('invalid_string')]"
                  @keyup.enter="scope.set"
                  @update:model-value="newName = scope.value"
                />
              </q-popup-edit>
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
            />
          </div>
        </q-td>
      </template>
      <!-- Info -->
      <template #body-cell-info="props">
        <q-td
          :props="props"
          auto-width
        >
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
            :rows-per-page-options="[0]"
            :rows="selectorRows"
            :columns="selectorColumns"
            filter="folder"
            :filter-method="filterFiles"
            row-key="name"
            @row-click="onSelectorRowClick"
          >
            <!-- Back Button/Header -->
            <template #top-left>
              <div>
                {{ $t('Select a folder') }}
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
            flat
            :label="$t('cancel')"
            color="primary"
            v-close-popup
          />
          <q-btn
            flat
            label="move"
            color="primary"
            v-close-popup
            @click="moveCopyItem('move')"
          />
          <q-btn
            flat
            label="copy"
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
    const windowHostname = ref<string>(window.location.origin)

    const columns = [
      {
        name: 'name',
        required: true,
        label: 'Name',
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
        label: 'Name',
        align: 'left',
        field: row => row.name,
        format: val => `${val}`
      }
    ]

    onMounted(() => {
      if (route.params.data) {
        chosenPath.value = `${route.params.data}/`
      }
      if (loginState) {
        rootPath.value = `/app/storage/${chosenPath.value}/`
      } else if (!loginState && chosenPath.value) {
        rootPath.value = `/app/storage/${chosenPath.value}/`
      } else {
        rootPath.value = '/app/storage/fileshare/'
      }
      updateRows()
    })

    function checkCharacters (files) {
      return files.filter(file => !invalidCharacters.value.some(el => file.name.includes(el)))
    }

    function checkUploadOverwrite (files) {
      for (let i = 0; i < files.length; i++) {
        if (rows.value.some(({ name }) => name === files[i].name)) {
          $q.notify({
            type: 'warning',
            message: 'Some of the files you added already exist.'
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
            cancel: true,
            persistent: true
          }).onOk(() => resolve(true)).onCancel(() => resolve(false)))) {
            return true
          } else {
            return false
          }
        }
      } return true
    }

    async function deleteFile (itemObj) {
      await Axios.post(`${api.value}/v1/filemanager/delete`, {
        path: objPath.value,
        object: itemObj,
        root: rootPath.value
      })
      selected.value = []
      updateRows()
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
        updateRows()
      }
    }

    function newFolderPrompt () {
      $q.dialog({
        title: 'Choose a name',
        message: 'Enter Folder Name',
        prompt: {
          model: '',
          isValid: val => val !== '',
          type: 'text'
        },
        cancel: true
      }).onOk(async data => {
        if (invalidCharacters.value.some(el => data.includes(el))) {
          $q.notify({
            type: 'negative',
            message: 'Filename did not pass validation constraints'
          })
        } else {
          if (checkRowExistence(data)) {
            $q.notify({
              type: 'negative',
              message: 'Folder already exists'
            })
          } else {
            await Axios.post(`${api.value}/v1/filemanager/newfolder`, {
              path: objPath.value,
              directory: data,
              root: rootPath.value
            })
            updateRows()
          }
        }
      })
    }

    function onRejected (rejectedEntries) {
      $q.notify({
        type: 'negative',
        message: `${rejectedEntries.length} file(s) did not pass validation constraints`
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
          message: 'Folder already exists'
        })
      } else {
        if (renameValid.value.validate()) {
          await Axios.post(`${api.value}/v1/filemanager/rename`, {
            path: objPath.value,
            from: currentName,
            to: newName,
            root: rootPath.value
          })
        }
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
      updateRows()
      unzipLoading.value = false
    }

    async function updateRows () {
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
    }

    async function updateSelectorRows () {
      await Axios.post(`${api.value}/v1/filemanager/list`, {
        path: selectorObjPath.value,
        root: rootPath.value
      }).then((response) => {
        selectorRows.value = response.data.rows
      }).catch(function (error) {
        console.log(error)
        $q.notify({ type: 'negative', message: t('error') })
      })
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
      loadingFileSize,
      loginState,
      loginToken,
      moveCopyItem,
      newFolderPrompt,
      newName: ref<any>(''),
      objPath,
      onRejected,
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
      visibleColumns: ref(['move', 'rename', 'delete', 'info'])
    }
  }
})

</script>

<style scoped>

</style>
