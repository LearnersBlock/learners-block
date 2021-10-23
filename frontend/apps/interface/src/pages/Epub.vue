<template>
  <q-page>
    <div
      v-touch-swipe.mouse.left.right.up="touchMoveToPage"
      style="position: absolute;z-index: 2000 !important; height: 67vh; width: 96%"
    />
    <div
      id="epub-render"
      class="bg-white"
      :style="'height: ' + $q.screen.height + 'px;'"
    />
    <q-page-sticky
      v-if="showMenu && !loading"
      style="z-index: 2001;"
      position="bottom-right"
      :offset="fabPos"
    >
      <q-fab
        v-if="!$q.fullscreen.isActive"
        v-model="fabRight"
        v-touch-pan.prevent.mouse="moveFab"
        vertical-actions-align="right"
        color="white"
        padding="xs"
        icon="keyboard_arrow_up"
        text-color="primary"
        direction="up"
        :disable="draggingFab"
      >
        <q-fab-action
          label-position="left"
          color="primary"
          icon="arrow_back"
          text-color="white"
          :label="$t('back')"
          :disable="draggingFab"
          @click="$router.back()"
        />
        <q-fab-action
          label-position="left"
          color="primary"
          icon="minimize"
          text-color="white"
          :label="$t('hide_button')"
          :disable="draggingFab"
          @click="hideMenu"
        />
        <q-fab-action
          label-position="left"
          color="primary"
          text-color="white"
          class="material-icons"
          icon="file_download"
          :label="$t('download')"
          :disable="draggingFab"
          @click="download"
        />
        <q-fab-action
          v-if="$q.fullscreen.isCapable"
          label-position="left"
          color="primary"
          :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
          text-color="white"
          :label="$t('full_screen')"
          :disable="draggingFab"
          @click="toggle"
        />
        <q-btn
          no-caps
          fab-mini
          no-wrap
          color="primary"
          icon-right="menu_book"
          :label="$t('select_chapter')"
          :disable="draggingFab"
          rounded
        >
          <q-menu>
            <q-list>
              <q-item
                v-for="i in tableOfContents"
                :key="i['href']"
                v-close-popup
                clickable
                @click="goToExcerpt(i)"
              >
                <q-item-section>{{ i['label'] }}</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </q-fab>
    </q-page-sticky>
    <q-inner-loading :showing="loading">
      <q-spinner
        size="5em"
        color="primary"
      />
    </q-inner-loading>
  </q-page>
</template>

<script lang="ts">
import ePub from 'epubjs'
import { useQuasar } from 'quasar'
import { defineComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const route = useRoute()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    // Import ePubJS
    const ePubJs = (ePub as any)

    // Set constants
    const draggingFab = ref<boolean>(false)
    const epubFile = ref<any>(route.query.url)
    const fabPos = ref<any>([7, 7])
    const fabRight = ref<boolean>(false)
    const loading = ref<boolean>(true)
    const showMenu = ref<boolean>(true)
    const tableOfContents = ref<Array<any>>([])

    // Fix for Safari where first page is not stored on load
    watch(() => $q.fullscreen.isActive, val => {
      if (val) {
        if (!ePubJs.rendition.location) {
          ePubJs.rendition.display()
        }
      }
    })

    onMounted(() => {
      loadEpub()
    })

    function download () {
      location.href = epubFile.value
    }

    function goToExcerpt (i) {
      ePubJs.rendition.display(i.href)
    }

    function hideMenu () {
      showMenu.value = false
      $q.notify({ type: 'info', multiLine: true, message: t('swipe_up_for_menu') })
    }

    function loadEpub () {
      if (!epubFile.value) {
        $q.notify({
          type: 'negative',
          timeout: 0,
          message: `${t('error')} Did you pass a URL to a file?`
        })
        loading.value = false
        return
      }
      ePubJs.book = ePubJs(epubFile.value)
      ePubJs.book.loaded.navigation.then(({ toc }) => {
        tableOfContents.value = toc
      })
      ePubJs.rendition = ePubJs.book.renderTo('epub-render', {
        method: 'default',
        height: '100%',
        width: '96vw'
      })
      ePubJs.rendition.display()
      ePubJs.book.ready.then(() => {
        loading.value = false
        if (!$q.platform.is.mobile) {
          $q.notify({ type: 'info', multiLine: true, message: t('click_swipe_instruction') })
        } else {
          $q.notify({ type: 'info', multiLine: true, message: t('swipe_instruction') })
        }
      })
    }

    function moveFab (ev) {
      draggingFab.value = ev.isFirst !== true && ev.isFinal !== true
      fabPos.value = [
        fabPos.value[0] - ev.delta.x,
        fabPos.value[1] - ev.delta.y
      ]
    }

    function toggle () {
      $q.fullscreen.toggle()
        .then(() => {
          $q.notify({ type: 'info', multiLine: true, message: t('swipe_up_exit') })
        })
        .catch((err) => {
          console.error(err)
        })
    }

    function touchMoveToPage ({ ...info }) {
      if (info.direction === 'left') {
        ePubJs.rendition.next()
      } else if (info.direction === 'right') {
        ePubJs.rendition.prev()
      } else if (info.direction === 'up' && $q.fullscreen.isActive) {
        $q.fullscreen.toggle()
      } else if (info.direction === 'up' && !$q.fullscreen.isActive) {
        showMenu.value = true
      }
    }

    return {
      download,
      draggingFab,
      fabPos,
      fabRight,
      goToExcerpt,
      hideMenu,
      loading,
      moveFab,
      showMenu,
      tableOfContents,
      toggle,
      touchMoveToPage
    }
  }
})
</script>
