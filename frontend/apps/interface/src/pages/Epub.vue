<template>
  <q-page>
    <div v-if="show">
      <div
        v-touch-swipe.mouse.left.right.up="touchMoveToPage"
        style="position: absolute;z-index: 2000 !important; height: 67vh; width: 96%"
      />
      <div
        class="bg-white"
        :style="'height: ' + this.$q.screen.height + 'px;'"
        id="epub-render"
      />
      <q-page-sticky
        style="z-index: 2001;"
        position="bottom-right"
        :offset="fabPos"
        v-if="this.showMenu"
      >
        <q-fab
          v-if="!this.$q.fullscreen.isActive"
          v-model="fabRight"
          vertical-actions-align="right"
          color="white"
          padding="xs"
          icon="keyboard_arrow_up"
          text-color="primary"
          direction="up"
          :disable="draggingFab"
          v-touch-pan.prevent.mouse="moveFab"
        >
          <q-fab-action
            label-position="left"
            @click="redirect"
            color="primary"
            text-color="white"
            class="material-icons"
            icon="arrow_back_ios"
            :label="$t('back')"
            :disable="draggingFab"
          />
          <q-fab-action
            label-position="left"
            color="primary"
            icon="minimize"
            text-color="white"
            @click="hideMenu"
            :label="$t('hide_button')"
            :disable="draggingFab"
          />
          <q-fab-action
            v-if="this.$q.fullscreen.isCapable"
            label-position="left"
            color="primary"
            :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
            text-color="white"
            @click="toggle"
            :label="$t('full_screen')"
            :disable="draggingFab"
          />
          <q-btn
            no-caps
            fab-mini
            no-wrap
            color="primary"
            icon-right="menu_book"
            :label="$t('chapter')"
            :disable="draggingFab"
            rounded
          >
            <q-menu>
              <q-list>
                <q-item
                  clickable
                  v-close-popup
                  v-for="i in toc"
                  :key="i['href']"
                  @click="goToExcerpt(i)"
                >
                  <q-item-section>{{ i['label'] }}</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </q-fab>
      </q-page-sticky>
      <q-inner-loading :showing="!show">
        <q-spinner
          size="5em"
          color="primary"
        />
      </q-inner-loading>
    </div>
  </q-page>
</template>

<script>
import ePub from 'epubjs'
import { watch, ref } from 'vue'

export default {
  name: 'EpubReader',
  data () {
    watch(() => this.$q.fullscreen.isActive, val => {
      // Fix for Safari where first page is not stored on load
      if (val) {
        if (!this.rendition.location) {
          this.rendition.display()
        }
      }
    })
    return {
      fabRight: ref(false),
      newEpub: [],
      show: false,
      book: {},
      rendition: {},
      chapter: '',
      toc: [],
      fabPos: [7, 7],
      draggingFab: false,
      showMenu: true
    }
  },
  mounted () {
    this.loadEpub()
    if (this.$q.platform.is.mobile) {
      this.$q.notify({ type: 'info', multiLine: true, message: this.$t('swipe_instruction') })
    } else {
      this.$q.notify({ type: 'info', multiLine: true, message: this.$t('click_swipe_instruction') })
    }
  },
  methods: {
    hideMenu () {
      this.showMenu = false
      this.$q.notify({ type: 'info', multiLine: true, message: this.$t('swipe_up_for_menu') })
    },
    toggle () {
      this.$q.fullscreen.toggle()
        .then(() => {
          this.$q.notify({ type: 'info', multiLine: true, message: this.$t('swipe_up_exit') })
        })
        .catch((err) => {
          alert(err)
          console.error(err)
        })
    },
    moveFab (ev) {
      this.draggingFab = ev.isFirst !== true && ev.isFinal !== true

      this.fabPos = [
        this.fabPos[0] - ev.delta.x,
        this.fabPos[1] - ev.delta.y
      ]
    },
    loadEpub (e) {
      const epub = this.$route.query.url
      if (!epub) {
        this.$q.notify({ type: 'negative', message: `${this.$t('error')} Did you pass a URL to a file?` })
        this.show = true
        return
      }
      this.book = ePub(e ? e.target.result : epub)
      this.book.loaded.navigation.then(({ toc }) => {
        this.toc = toc
      })
      this.book.ready.then(() => {
        this.show = true
      })
      this.rendition = this.book.renderTo('epub-render', {
        method: 'default',
        height: '100%',
        width: '96vw'
      })
      this.rendition.display()
      document.getElementById('add')
    },
    redirect () {
      location.href = '/'
    },
    nextPage () {
      this.rendition.next()
    },
    previousPage () {
      this.rendition.prev()
    },
    touchMoveToPage ({ ...info }) {
      if (info.direction === 'left') {
        this.nextPage()
      } else if (info.direction === 'right') {
        this.previousPage()
      } else if (info.direction === 'up' && this.$q.fullscreen.isActive) {
        this.$q.fullscreen.toggle()
      } else if (info.direction === 'up' && !this.$q.fullscreen.isActive) {
        this.showMenu = true
      }
    },
    goToExcerpt (i) {
      this.rendition.display(i.href)
    }
  }
}
</script>
