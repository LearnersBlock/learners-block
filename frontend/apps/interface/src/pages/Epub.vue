<template>
  <q-page padding>
    <div
      class="row col-12"
      v-if="show"
    >
      <q-select
        class="col mt-1 ml-1"
        filled
        v-model="chapter"
        :options="toc"
        :label="$t('chapter')"
        dense
        option-value="href"
        option-label="label"
        option-disable="inactive"
        emit-value
        map-options
        @update:model-value="goToExcerpt"
      />
    </div>
    <div>
      <div
        class="col-12"
        v-touch-swipe.mouse.left.right="touchMoveToPage"
        style="position: absolute;z-index: 2000 !important; height: 67vh; width: 96%"
      />
    </div>
    <div
      class="reader"
      id="epub-render"
    />
    <q-inner-loading :showing="!show">
      <q-spinner
        size="5rem"
        color="primary"
      />
    </q-inner-loading>
  </q-page>
</template>

<script>
import ePub from 'epubjs'

export default {
  name: 'EpubReader',
  data () {
    return {
      newEpub: [],
      show: false,
      book: {},
      rendition: {},
      chapter: '',
      toc: []
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
    loadEpub (e) {
      const epub = this.$route.query.url
      if (!epub) {
        this.$q.notify({ type: 'negative', message: this.$t('error') })
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
    nextPage () {
      this.rendition.next()
    },
    previousPage () {
      this.rendition.prev()
    },
    touchMoveToPage ({ ...info }) {
      if (info.direction === 'left') {
        this.nextPage()
      } else {
        this.previousPage()
      }
    },
    goToExcerpt () {
      if (Number.isInteger(this.chapter.toLowerCase().indexOf('xhtml'))) {
        this.rendition.display(this.chapter)
      } else {
        this.rendition.display(`epubcfi(${this.chapter})`)
      }
    }
  }
}
</script>

<style scoped lang="scss">
.reader {
  height: calc(100vh - 145px);
}

</style>
