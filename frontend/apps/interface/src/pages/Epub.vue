<template>
  <q-page padding>
    <div
      class="row"
      v-if="show"
    >
      <div class="col-12 q-pt-sm">
        <q-select
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
    </div>
    <div
      class="col-12"
      v-touch-swipe.mouse.left.right="touchMoveToPage"
    />
    <div id="epub-render" />
    <div
      class="row q-gutter-md q-px-sm"
      v-if="show"
    >
      <q-btn
        @click="previousPage()"
        icon="arrow_left"
        :label="$t('previous')"
        class="col"
        dense
      />
      <q-btn
        @click="nextPage()"
        icon-right="arrow_right"
        :label="$t('next')"
        class="col"
        dense
      />
    </div>
    <q-inner-loading :showing="!show">
      <q-spinner-gears
        size="50px"
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
  },
  methods: {
    loadEpub (e) {
      const epub = this.$route.query.url
      if (!epub) {
        this.$q.notify({ type: 'negative', message: this.$t('error') })
      }
      this.book = ePub(e ? e.target.result : epub)
      this.book.loaded.navigation.then(({ toc }) => {
        this.toc = toc
      })
      this.book.ready.then(() => {
        this.show = true
      })
      this.rendition = this.book.renderTo('epub-render', {
        height: '70vh',
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
        this.rendition.annotations.highlight(`epubcfi(${this.chapter})`)
      }
    }
  }
}
</script>
