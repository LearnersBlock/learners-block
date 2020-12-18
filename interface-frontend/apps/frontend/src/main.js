import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './i18n'

import {
    Alert,
    Container,
    Header,
    Main,
    Button,
    Dialog,
    Loading,
    Form,
    FormItem,
    Radio,
    RadioButton,
    Input,
    Select,
    Option,
    Switch,
    Table,
    TableColumn
} from 'element-ui'

import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'

Vue.use(Container)
Vue.use(Header)
Vue.use(Main)
Vue.use(Button)
Vue.use(Dialog)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Radio)
Vue.use(RadioButton)
Vue.use(Switch)
Vue.use(Select)
Vue.use(Option)
Vue.use(Alert)
Vue.use(Loading)
Vue.use(Table)
Vue.use(TableColumn)

locale.use(lang)

Vue.config.productionTip = false
Vue.$router = router

new Vue({
    router,
    store,
    i18n,
    render: h => h(App)
}).$mount('#app')
